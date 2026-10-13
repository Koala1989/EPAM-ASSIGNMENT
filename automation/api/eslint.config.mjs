import tseslint from 'typescript-eslint';
import playwright from 'eslint-plugin-playwright';

const httpCall = /^(get|post|put|patch|delete|head|fetch)$/;

// no-restricted-syntax is replaced, not merged, by a later matching block: each group lists its full set.
const noUrls = [
  { selector: 'Literal[value=/https?:\\/\\//]', message: 'No hosts or full URLs; the base URL comes from config/env.ts (CONVENTIONS.md §7).' },
  { selector: 'TemplateElement[value.raw=/https?:\\/\\//]', message: 'No hosts or full URLs; the base URL comes from config/env.ts (CONVENTIONS.md §7).' },
];
const specRules = [
  {
    selector: `CallExpression[callee.property.name=${httpCall}]`,
    message: 'Specs must not send requests directly; call a client method, or add one (CONVENTIONS.md §3).',
  },
  { selector: "ImportDeclaration[source.value='@playwright/test']", message: 'Import test and expect from the fixtures (CONVENTIONS.md §5).' },
];
const clientRules = [{ selector: "ImportSpecifier[imported.name='expect']", message: 'Clients never assert (CONVENTIONS.md §4).' }];

export default tseslint.config(
  { ignores: ['node_modules/**', 'playwright-report/**', 'test-results/**'] },
  ...tseslint.configs.recommended,
  {
    ...playwright.configs['flat/recommended'],
    files: ['tests/**/*.ts', 'fixtures/**/*.ts'],
  },
  {
    // Fixtures are not tests: Playwright's test-structure rules do not apply to them.
    files: ['fixtures/**/*.ts'],
    rules: { 'playwright/no-standalone-expect': 'off', 'playwright/no-conditional-in-test': 'off' },
  },
  {
    // CONVENTIONS.md §7: no hosts or full URLs outside config/env.ts.
    files: ['tests/**/*.ts', 'fixtures/**/*.ts', 'utils/**/*.ts'],
    rules: { 'no-restricted-syntax': ['error', ...noUrls] },
  },
  {
    // CONVENTIONS.md §3: specs call clients, never the request context directly.
    files: ['tests/**/*.spec.ts'],
    rules: { 'no-restricted-syntax': ['error', ...specRules, ...noUrls] },
  },
  {
    // CONVENTIONS.md §4: clients send requests; they never assert.
    files: ['clients/**/*.ts'],
    rules: { 'no-restricted-syntax': ['error', ...clientRules, ...noUrls] },
  },
  {
    files: ['**/*.ts'],
    rules: {
      'no-restricted-properties': [
        'error',
        { object: 'process', property: 'env', message: 'Read environment values through config/env.ts (CONVENTIONS.md §7).' },
      ],
    },
  },
  {
    files: ['config/env.ts', 'playwright.config.ts'],
    rules: { 'no-restricted-properties': 'off' },
  },
);
