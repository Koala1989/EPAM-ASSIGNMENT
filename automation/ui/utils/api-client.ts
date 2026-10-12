import { request, APIRequestContext } from '@playwright/test';

/** An APIRequestContext for `${baseURL}/api/` authenticated with the user's InvenTree token. */
export async function createApiContext(baseURL: string, username: string, password: string): Promise<APIRequestContext> {
  const basic = Buffer.from(`${username}:${password}`).toString('base64');
  const anon = await request.newContext({ baseURL });
  const res = await anon.get('/api/user/me/token/', { headers: { Authorization: `Basic ${basic}` } });
  if (!res.ok()) throw new Error(`Token for ${username}: HTTP ${res.status()} ${await res.text()}`);
  const { token } = (await res.json()) as { token: string };
  await anon.dispose();
  return request.newContext({
    baseURL: `${baseURL}/api/`,
    extraHTTPHeaders: { Authorization: `Token ${token}`, Accept: 'application/json' },
  });
}
