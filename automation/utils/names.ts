import { randomBytes } from 'node:crypto';

export const qaSuffix = () => `QA-${randomBytes(4).toString('hex').toUpperCase()}`;

export const qaName = (suffix: string, label: string) => `${suffix} ${label}`;

export const slug = (label: string) => label.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
