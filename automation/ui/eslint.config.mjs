import tseslint from 'typescript-eslint';
import playwright from 'eslint-plugin-playwright';

const rawLocator = /^(locator|getByRole|getByLabel|getByText|getByPlaceholder|getByTestId|getByAltText|getByTitle|\$|\$\$)$/;

export default tseslint.config(
  { ignores: ['node_modules/**', 'playwright-report/**', 'test-results/**', 'playwright/**'] },
  ...tseslint.configs.recommended,
  {
    ...playwright.configs['flat/recommended'],
    files: ['tests/**/*.ts', 'pages/**/*.ts', 'fixtures/**/*.ts'],
  },
  {
    // CONVENTIONS.md §8: forbidden outright, not just discouraged.
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
    // CONVENTIONS.md §3: specs use page objects, never raw locators.
    files: ['tests/**/*.spec.ts'],
    rules: {
      'no-restricted-syntax': [
        'error',
        {
          selector: `CallExpression[callee.property.name=${rawLocator}]`,
          message: 'Specs must not query the DOM directly; add a locator or action to a page object (CONVENTIONS.md §3).',
        },
        {
          selector: "ImportDeclaration[source.value='@playwright/test']",
          message: "Import test and expect from the fixtures (CONVENTIONS.md §5).",
        },
      ],
    },
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
