import type { Adapter } from "@auth/core/adapters";

/**
 * Adapter for django-authjs.
 *
 * @param url - Backend server auth endpoint.
 * @returns Auth.js adapter
 */
export function DjangoAdapter(url: string | URL): Adapter;
