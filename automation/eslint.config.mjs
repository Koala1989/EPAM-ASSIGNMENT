import tseslint from 'typescript-eslint';
import playwright from 'eslint-plugin-playwright';

// Section references are to CONVENTIONS.md: "UI §n" and "API §n" are the UI and API parts.
const rawLocator = /^(locator|getByRole|getByLabel|getByText|getByPlaceholder|getByTestId|getByAltText|getByTitle|\$|\$\$)$/;
const httpCall = /^(get|post|put|patch|delete|head|fetch)$/;

// no-restricted-syntax is replaced, not merged, by a later matching block: each group lists its full set.
const noUrls = [
  { selector: 'Literal[value=/https?:\\/\\//]', message: 'No hosts or full URLs; the base URL comes from config/env.ts (CONVENTIONS.md, Shared §3).' },
  { selector: 'TemplateElement[value.raw=/https?:\\/\\//]', message: 'No hosts or full URLs; the base URL comes from config/env.ts (CONVENTIONS.md, Shared §3).' },
];
const fixtureImport = { selector: "ImportDeclaration[source.value='@playwright/test']", message: 'Import test and expect from the fixtures (CONVENTIONS.md UI §5, API §5).' };
const uiSpecRules = [
  { selector: `CallExpression[callee.property.name=${rawLocator}]`, message: 'Specs must not query the DOM directly; add a locator or action to a page object (CONVENTIONS.md UI §3).' },
  fixtureImport,
];
const apiSpecRules = [
  { selector: `CallExpression[callee.property.name=${httpCall}]`, message: 'Specs must not send requests directly; call a client method, or add one (CONVENTIONS.md API §3).' },
  fixtureImport,
];
const clientRules = [{ selector: "ImportSpecifier[imported.name='expect']", message: 'Clients never assert (CONVENTIONS.md API §4).' }];

export default tseslint.config(
  { ignores: ['node_modules/**', 'playwright-report/**', 'test-results/**', 'playwright/**'] },
  ...tseslint.configs.recommended,
  {
    ...playwright.configs['flat/recommended'],
    files: ['tests/**/*.ts', 'pages/**/*.ts', 'fixtures/**/*.ts'],
  },
  {
    // UI §8: forbidden outright, not just discouraged.
    files: ['tests/**/*.ts', 'pages/**/*.ts', 'fixtures/**/*.ts'],
    rules: {
      'playwright/no-wait-for-timeout': 'error',
      'playwright/no-networkidle': 'error',
      'playwright/no-force-option': 'error',
    },
  },
  {
    // Page objects and fixtures are not tests: Playwright's test-structure rules do not apply to them.
    files: ['pages/**/*.ts', 'fixtures/**/*.ts'],
    rules: { 'playwright/no-standalone-expect': 'off', 'playwright/no-conditional-in-test': 'off' },
  },
  {
    // Shared §3: no hosts or full URLs outside config/. UI specs are exempt: a URL there is test data typed into a
    // field (e.g. the part's Link), never the app's address, which page objects never use either.
    files: ['tests/api/**/*.ts', 'pages/**/*.ts', 'fixtures/**/*.ts', 'utils/**/*.ts'],
    rules: { 'no-restricted-syntax': ['error', ...noUrls] },
  },
  {
    // UI §3: UI specs use page objects, never raw locators.
    files: ['tests/ui/**/*.spec.ts'],
    rules: { 'no-restricted-syntax': ['error', ...uiSpecRules] },
  },
  {
    // API §3: API specs call clients, never the request context directly.
    files: ['tests/api/**/*.spec.ts'],
    rules: { 'no-restricted-syntax': ['error', ...apiSpecRules, ...noUrls] },
  },
  {
    // API §4: clients send requests; they never assert.
    files: ['clients/**/*.ts'],
    rules: { 'no-restricted-syntax': ['error', ...clientRules, ...noUrls] },
  },
  {
    files: ['**/*.ts'],
    rules: {
      'no-restricted-properties': [
        'error',
        { object: 'process', property: 'env', message: 'Read environment values through config/env.ts (CONVENTIONS.md, Shared §3).' },
      ],
    },
  },
  {
    files: ['config/env.ts', 'playwright.config.ts'],
    rules: { 'no-restricted-properties': 'off' },
  },
);
