const number = (value: string | undefined, fallback: number) => (value ? Number(value) : fallback);

const baseURL = (process.env.INVENTREE_URL ?? 'http://localhost').replace(/\/$/, '');

export const env = {
  baseURL,
  apiURL: `${baseURL}/api/`,
  testTimeout: number(process.env.TEST_TIMEOUT_MS, 60_000),
  expectTimeout: number(process.env.EXPECT_TIMEOUT_MS, 30_000),
};

// Defaults are the published passwords of InvenTree's demo dataset on the local Docker instance.
const demoPasswords: Record<string, string> = {
  admin: 'inventree',
  allaccess: 'nolimits',
  engineer: 'partsonly',
  reader: 'readonly',
  noaccess: 'youshallnotpass',
  steven: 'wizardstaff',
};

export function passwordFor(username: string): string {
  const password = process.env[`INVENTREE_${username.toUpperCase()}_PASSWORD`] ?? demoPasswords[username];
  if (!password) throw new Error(`No password for user "${username}": set INVENTREE_${username.toUpperCase()}_PASSWORD`);
  return password;
}
