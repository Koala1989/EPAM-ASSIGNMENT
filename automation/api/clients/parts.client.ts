import { APIRequestContext } from '@playwright/test';
import { ResourceClient } from './base.client';

/** /api/part/ */
export class PartsClient extends ResourceClient {
  constructor(api: APIRequestContext) {
    super(api, 'part/');
  }
}
