import { request, APIRequestContext } from '@playwright/test';
import { credentialsFor, env, type UserName } from '../config/env';

const tokens = new Map<string, string>();

function basicAuth(user: UserName) {
  const { username, password } = credentialsFor(user);
  return `Basic ${Buffer.from(`${username}:${password}`).toString('base64')}`;
}

/** The user's InvenTree API token from GET /api/user/me/token/, cached per worker. */
export async function tokenFor(username: UserName): Promise<string> {
  const cached = tokens.get(username);
  if (cached) return cached;
  const anon = await request.newContext({ baseURL: env.apiURL });
  try {
    const res = await anon.get('user/me/token/', { headers: { Authorization: basicAuth(username) } });
    if (!res.ok()) throw new Error(`Token for ${username}: HTTP ${res.status()} ${await res.text()}`);
    const { token } = (await res.json()) as { token: string };
    tokens.set(username, token);
    return token;
  } finally {
    await anon.dispose();
  }
}

/** An APIRequestContext on `<baseURL>/api/`, sending `Authorization: Token <token>`, or no credentials when token is undefined. */
export async function apiContext(token?: string): Promise<APIRequestContext> {
  return request.newContext({
    baseURL: env.apiURL,
    extraHTTPHeaders: { Accept: 'application/json', ...(token ? { Authorization: `Token ${token}` } : {}) },
  });
}

/** Basic-auth header for a demo user; for the token endpoint only. */
export const basicAuthHeader = basicAuth;
