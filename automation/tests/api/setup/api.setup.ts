import { test, expect } from '../../../fixtures';
import { userNames } from '../../../config/env';

// Runs before the API specs (project api-smoke): the instance is reachable, every demo user can get a token,
// and the schema validator accepts a real response. Saves nothing.
for (const username of userNames) {
  test(`token for ${username}`, async ({ apiAs }) => {
    const anonymous = await apiAs('anonymous');
    const res = await anonymous.auth.requestToken(username);
    await expect(res).toHaveStatus(200);
    expect((await res.json()).token).toEqual(expect.any(String));
  });
}

test('schema validator accepts a real category list', async ({ apiAs }) => {
  const admin = await apiAs('admin');
  const res = await admin.categories.list({ limit: 5 });
  await expect(res).toHaveStatus(200);
  await expect(res).toMatchSchema('PaginatedCategoryList');
  await expect({ count: 'not a number', results: [] }).not.toMatchSchema('PaginatedCategoryList');
});
