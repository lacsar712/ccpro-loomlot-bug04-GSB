import { get } from 'svelte/store';
import { token, clearSession } from './auth.js';

export async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (!(options.body instanceof URLSearchParams) && options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }
  const t = get(token);
  if (t) headers.Authorization = `Bearer ${t}`;

  const res = await fetch(`/api${path}`, { ...options, headers });

  if (res.status === 401) {
    clearSession();
    throw new Error('未登录或登录已过期');
  }

  const text = await res.text();
  let data = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!res.ok) {
    const msg =
      (data && data.detail) ||
      (typeof data === 'string' ? data : null) ||
      `请求失败 (${res.status})`;
    throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }

  return data;
}

export function toLocalInput(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export function fromLocalInput(val) {
  return new Date(val).toISOString();
}

export const VAT_STATUS = {
  ready: '就绪',
  dyeing: '染色中',
  drain: '排液',
};
