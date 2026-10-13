import { expect as base, APIResponse } from '@playwright/test';
import { knownDefect, schemaErrors } from '../utils/schema';

async function bodyOf(received: unknown) {
  return received && typeof (received as APIResponse).json === 'function' ? (received as APIResponse).json() : received;
}

export const expect = base.extend({
  /** The response has exactly this status code. On failure the message shows the response body. */
  async toHaveStatus(response: APIResponse, expected: number) {
    const actual = response.status();
    const pass = actual === expected;
    const text = pass ? '' : (await response.text()).slice(0, 1000);
    return {
      pass,
      name: 'toHaveStatus',
      expected,
      actual,
      message: () =>
        `${this.utils.matcherHint('toHaveStatus', undefined, undefined, { isNot: this.isNot })}\n\n` +
        `Expected status: ${this.isNot ? 'not ' : ''}${expected}\nReceived status: ${actual}` +
        (text ? `\nResponse body: ${text}` : ''),
    };
  },

  /**
   * The response body (or an already parsed value) is valid against components.schemas.<component> of openapi-parts.yaml.
   * Use it with expect.soft (CONVENTIONS §5): a schema defect is reported without stopping the test's other checks.
   * Each error is labelled with the finding that explains it, or NEW when none does.
   */
  async toMatchSchema(received: unknown, component: string) {
    const errors = schemaErrors(component, await bodyOf(received));
    const pass = errors.length === 0;
    const findings = [...new Set(errors.map((e) => knownDefect(e) ?? 'NEW'))];
    const summary = findings.includes('NEW')
      ? 'Includes errors no finding explains (NEW).'
      : `Known product defects only: ${findings.join(', ')} (test-cases/findings.md).`;
    return {
      pass,
      name: 'toMatchSchema',
      message: () =>
        `${this.utils.matcherHint('toMatchSchema', undefined, component, { isNot: this.isNot })}\n\n` +
        (pass
          ? `Expected the body not to match ${component}`
          : `Body does not match ${component}. ${summary}\n  ` +
            errors.slice(0, 15).map((e) => `[${knownDefect(e) ?? 'NEW'}] ${e}`).join('\n  ')),
    };
  },
});
