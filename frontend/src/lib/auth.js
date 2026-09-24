import { writable } from 'svelte/store';

const TOKEN_KEY = 'loomlot_token';
const USER_KEY = 'loomlot_user';

function load(key, fallback = null) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

export const token = writable(localStorage.getItem(TOKEN_KEY) || '');
export const user = writable(load(USER_KEY));

export function setSession(accessToken, userData) {
  localStorage.setItem(TOKEN_KEY, accessToken);
  localStorage.setItem(USER_KEY, JSON.stringify(userData));
  token.set(accessToken);
  user.set(userData);
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  token.set('');
  user.set(null);
}
