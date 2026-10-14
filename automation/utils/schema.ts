import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import Ajv, { ValidateFunction } from 'ajv';
import addFormats from 'ajv-formats';
import { parse } from 'yaml';

const SCHEMA_FILE = resolve(__dirname, '../../requirements/openapi-parts.yaml');

// OpenAPI 3.0 `nullable` is not JSON Schema: rewrite it as "the schema, or null".
function toJsonSchema(node: unknown): unknown {
  if (Array.isArray(node)) return node.map(toJsonSchema);
  if (!node || typeof node !== 'object') return node;
  const source = node as Record<string, unknown>;
  const out: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(source)) if (key !== 'nullable') out[key] = toJsonSchema(value);
  return source.nullable === true ? { anyOf: [out, { type: 'null' }] } : out;
}

let ajv: Ajv | undefined;
const validators = new Map<string, ValidateFunction>();

function validator(component: string): ValidateFunction {
  if (!ajv) {
    const doc = parse(readFileSync(SCHEMA_FILE, 'utf8')) as { components: { schemas: Record<string, unknown> } };
    ajv = new Ajv({ strict: false, allErrors: true });
    addFormats(ajv);
    // OpenAPI numeric and binary formats carry no extra constraint for JSON values.
    for (const format of ['double', 'float', 'int32', 'int64', 'decimal', 'binary', 'byte']) ajv.addFormat(format, true);
    ajv.addSchema({ $id: 'openapi', components: toJsonSchema(doc.components) });
  }
  let validate = validators.get(component);
  if (!validate) {
    validate = ajv.compile({ $ref: `openapi#/components/schemas/${component}` });
    validators.set(component, validate);
  }
  return validate;
}

/**
 * Schema errors caused by product defects already recorded in test-cases/findings.md. Used only to label a
 * failure; the error still fails the check. Add an entry when a new schema defect is recorded.
 */
const KNOWN_DEFECTS: { finding: string; error: RegExp }[] = [
  { finding: 'F-06', error: /\/image must match format "uri"/ },
  { finding: 'F-07', error: /\/availability_updated must / },
  { finding: 'F-11', error: /must have required property 'category_name'/ },
  { finding: 'F-12', error: /\/pricing_updated must / },
];

/** The finding a schema error line belongs to, or undefined for an error no finding explains. */
export function knownDefect(error: string): string | undefined {
  return KNOWN_DEFECTS.find((d) => d.error.test(error))?.finding;
}

/** Validates `body` against `components.schemas.<component>` of requirements/openapi-parts.yaml; returns error lines, empty if valid. */
export function schemaErrors(component: string, body: unknown): string[] {
  const validate = validator(component);
  if (validate(body)) return [];
  return (validate.errors ?? []).map((e) => `${e.instancePath || '(root)'} ${e.message ?? e.keyword}`);
}
