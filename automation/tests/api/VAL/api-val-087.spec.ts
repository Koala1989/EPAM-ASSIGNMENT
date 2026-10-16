// case: test-cases/API_Field_Validation/part-name-validation-on-create.md (API-VAL-087)
import { test, expect } from '../../../fixtures';
import rows from '../../../data/api/VAL/api-val-087.json';

test.use({ user: 'engineer' });

test.describe('Part name validation on create', () => {
  for (const row of rows) {
    test(
      `API-VAL-087 [${row.label}]: Part name is validated on create (absent, null, blank, length boundaries)`,
      { tag: ['@smoke', '@regression'] },
      async ({ api, data }) => {
        const suffix = data.name('').trim();
        const tag = `${suffix} ${row.tag}`;
        const name =
          typeof row.name === 'string' ? row.name.replace('QA-<suffix>', suffix) + 'x'.repeat(row['name padding']) : row.name;
        // The name key is left out for the absent row.
        const nameField = row.name === '(key left out)' ? {} : { name };
        const payload = { ...nameField, description: tag };
        // Registered by its unique QA- name before the request, which may or may not create a part.
        // Blank, null and absent names are not unique, so for them the pk is tracked after a 201 (step 1).
        data.trackPart(`${suffix}${'x'.repeat(row['name padding'])}`);

        await test.step('1. POST /api/part/ as engineer', async () => {
          const res = await api.parts.create(payload);
          await expect(res).toHaveStatus(row['expected status']);
          if (row['expected status'] === 201) {
            const body = await res.json();
            data.trackPart(body.pk);
            await expect.soft(res).toMatchSchema('Part');
            expect(body.name).toBe(payload.name);
            expect(Number.isInteger(body.pk)).toBe(true);
          }
          // Error body and text for a rejected request: open (Q-VAL-01), not asserted.
        });

        await test.step('2. GET /api/part/ as engineer', async () => {
          const res = await api.parts.list({ search: tag, limit: 10 });
          await expect(res).toHaveStatus(200);
          const body = await res.json();
          expect(body.count).toBe(row.count);
        });
      },
    );
  }
});