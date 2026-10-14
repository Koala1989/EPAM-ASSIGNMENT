import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
// The local users file is the reference: every environment's users file must define the same user keys.
import referenceUsers from '../data/users.local.json';

/**
 * The one place that reads process.env, for the UI and API suites alike.
 *
 * TEST_ENV (default `local`) selects config/environments/<TEST_ENV>.json. Then config/.env.<TEST_ENV>, if present,
 * is loaded into process.env; variables already set in the shell or CI win over the file.
 */
const CONFIG = __dirname;
const DATA = resolve(__dirname, '../data');

type Environment = {
  description: string;
  baseURL: string;
  users: string;
  /** Only for the local demo dataset: fall back to its published passwords. */
  demoPasswords: boolean;
  testTimeoutMs: number;
  expectTimeoutMs: number;
};

export type UserName = keyof typeof referenceUsers;
export type User = { username: string; displayName: string; role: string; use: string };

/** An environment variable, treating an empty value (e.g. `INVENTREE_URL=` copied from .env.example) as unset. */
const read = (variable: string) => process.env[variable] || undefined;

const name = read('TEST_ENV') ?? 'local';
const environmentFile = resolve(CONFIG, 'environments', `${name}.json`);
if (!existsSync(environmentFile)) {
  const known = readdirSync(resolve(CONFIG, 'environments')).map((f) => f.replace(/\.json$/, ''));
  throw new Error(`TEST_ENV=${name}: no automation/config/environments/${name}.json. Known: ${known.join(', ')}`);
}
const environment = JSON.parse(readFileSync(environmentFile, 'utf8')) as Environment;

const dotenv = resolve(CONFIG, `.env.${name}`);
if (existsSync(dotenv)) process.loadEnvFile(dotenv);

const number = (value: string | undefined, fallback: number) => (value ? Number(value) : fallback);
const baseURL = (read('INVENTREE_URL') ?? environment.baseURL).replace(/\/$/, '');

export const env = {
  name,
  baseURL,
  apiURL: `${baseURL}/api/`,
  testTimeout: number(read('TEST_TIMEOUT_MS'), environment.testTimeoutMs),
  expectTimeout: number(read('EXPECT_TIMEOUT_MS'), environment.expectTimeoutMs),
};

/** This environment's test users, keyed by the name specs use: test.use({ user: 'engineer' }). */
export const users = JSON.parse(readFileSync(resolve(DATA, environment.users), 'utf8')) as Record<UserName, User>;
export const userNames = Object.keys(referenceUsers) as UserName[];
const missing = userNames.filter((u) => !users[u]);
if (missing.length) throw new Error(`${environment.users} (TEST_ENV=${name}) has no entry for: ${missing.join(', ')}`);

// The published passwords of InvenTree's demo dataset; used only when the environment sets demoPasswords.
const demoPasswords: Record<UserName, string> = {
  admin: 'inventree',
  allaccess: 'nolimits',
  engineer: 'partsonly',
  reader: 'readonly',
  noaccess: 'youshallnotpass',
  steven: 'wizardstaff',
};

/** Login name and password of a test user in this environment. Password: INVENTREE_<USER>_PASSWORD. */
export function credentialsFor(user: UserName): { username: string; password: string } {
  const variable = `INVENTREE_${user.toUpperCase()}_PASSWORD`;
  const password = read(variable) ?? (environment.demoPasswords ? demoPasswords[user] : undefined);
  if (!password) throw new Error(`No password for user "${user}" (TEST_ENV=${name}): set ${variable} or add it to automation/config/.env.${name}`);
  return { username: users[user].username, password };
}
