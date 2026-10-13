import { APIRequestContext } from '@playwright/test';
import { ResourceClient } from './base.client';

/** /api/company/part/ */
export class SupplierPartsClient extends ResourceClient {
  constructor(api: APIRequestContext) {
    super(api, 'company/part/');
  }
}
