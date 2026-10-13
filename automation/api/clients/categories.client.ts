import { APIRequestContext } from '@playwright/test';
import { ResourceClient } from './base.client';

/** /api/part/category/ */
export class CategoriesClient extends ResourceClient {
  constructor(api: APIRequestContext) {
    super(api, 'part/category/');
  }
}
