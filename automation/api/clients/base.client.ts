import { APIRequestContext, APIResponse } from '@playwright/test';

export type Json = Record<string, unknown>;
export type Query = Record<string, string | number | boolean>;

/**
 * One REST resource (a list endpoint plus its `<id>/` detail endpoint).
 * Methods send exactly what they are given and return the raw response, so specs can assert any
 * status code, including errors. Clients never assert and never fix up the data they send.
 */
export class ResourceClient {
  constructor(
    protected readonly api: APIRequestContext,
    protected readonly endpoint: string,
  ) {}

  /** GET the list endpoint with query parameters. */
  list(params: Query = {}): Promise<APIResponse> {
    return this.api.get(this.endpoint, { params });
  }

  /** POST a JSON body to the list endpoint. */
  create(body: unknown): Promise<APIResponse> {
    return this.api.post(this.endpoint, { data: body });
  }

  /** GET one record. */
  retrieve(id: number | string): Promise<APIResponse> {
    return this.api.get(this.detail(id));
  }

  /** PUT a full JSON body to one record. */
  update(id: number | string, body: unknown): Promise<APIResponse> {
    return this.api.put(this.detail(id), { data: body });
  }

  /** PATCH the given fields of one record. */
  partialUpdate(id: number | string, body: unknown): Promise<APIResponse> {
    return this.api.patch(this.detail(id), { data: body });
  }

  /** DELETE one record, with an optional JSON body. */
  destroy(id: number | string, body?: unknown): Promise<APIResponse> {
    return this.api.delete(this.detail(id), body === undefined ? undefined : { data: body });
  }

  protected detail(id: number | string) {
    return `${this.endpoint}${id}/`;
  }
}
