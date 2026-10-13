import { APIRequestContext, APIResponse } from '@playwright/test';
import type { UserName } from '../config/env';
import { basicAuthHeader } from '../utils/api-context';

/** /api/user/me/token/ */
export class AuthClient {
  constructor(private readonly api: APIRequestContext) {}

  /** GET the token endpoint with the demo user's basic-auth credentials. */
  requestToken(username: UserName): Promise<APIResponse> {
    return this.api.get('user/me/token/', { headers: { Authorization: basicAuthHeader(username) } });
  }

  /** GET the token endpoint with whatever credentials this client was created with. */
  currentToken(): Promise<APIResponse> {
    return this.api.get('user/me/token/');
  }
}
