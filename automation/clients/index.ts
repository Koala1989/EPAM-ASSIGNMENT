import { APIRequestContext } from '@playwright/test';
import { AuthClient } from './auth.client';
import { CategoriesClient } from './categories.client';
import { PartsClient } from './parts.client';
import { SupplierPartsClient } from './supplier-parts.client';

/** Every client, bound to one authenticated (or anonymous) request context. */
export type Clients = {
  parts: PartsClient;
  categories: CategoriesClient;
  supplierParts: SupplierPartsClient;
  auth: AuthClient;
};

export function clientsFor(api: APIRequestContext): Clients {
  return {
    parts: new PartsClient(api),
    categories: new CategoriesClient(api),
    supplierParts: new SupplierPartsClient(api),
    auth: new AuthClient(api),
  };
}

export type { Json, Query } from './base.client';
