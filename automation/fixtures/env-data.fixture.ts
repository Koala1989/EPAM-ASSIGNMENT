import { test as base } from '@playwright/test';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { env } from '../config/env';
// The local file is the reference: it gives EnvData its type, and every environment's file must have its keys.
import reference from '../data/partsAndCategories.local.json';

export type EnvData = typeof reference;

/** Keys of the reference that `actual` lacks, as dotted paths (e.g. "part.Displayname"). */
function missingKeys(ref: unknown, actual: unknown, path = ''): string[] {
  if (typeof ref !== 'object' || ref === null || Array.isArray(ref)) return [];
  const value = typeof actual === 'object' && actual !== null ? (actual as Record<string, unknown>) : {};
  return Object.entries(ref).flatMap(([key, child]) =>
    key in value ? missingKeys(child, value[key], `${path}${key}.`) : [`${path}${key}`],
  );
}

/**
 * `envData`: values that differ per environment, from data/partsAndCategories.<TEST_ENV>.json.
 * Worker-scoped: read once per worker. Lazy: a run that never asks for it never needs the file.
 */
// eslint-disable-next-line @typescript-eslint/no-empty-object-type -- no test-scoped fixtures, only a worker one
export const test = base.extend<{}, { envData: EnvData }>({
  envData: [
    async ({}, use) => {
      const file = resolve(__dirname, '../data', `partsAndCategories.${env.name}.json`);
      if (!existsSync(file)) {
        throw new Error(`TEST_ENV=${env.name}: no automation/data/partsAndCategories.${env.name}.json (copy the local one and set its values)`);
      }
      const data: unknown = JSON.parse(readFileSync(file, 'utf8'));
      const missing = missingKeys(reference, data);
      if (missing.length) throw new Error(`partsAndCategories.${env.name}.json has no entry for: ${missing.join(', ')}`);
      await use(data as EnvData);
    },
    { scope: 'worker' },
  ],
});
