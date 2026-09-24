<script>
  import { push } from 'svelte-spa-router';
  import { setSession, token } from '../lib/auth.js';

  let username = 'admin';
  let password = '123456';
  let error = '';
  let loading = false;

  $: if ($token) push('/');

  async function submit() {
    error = '';
    loading = true;
    try {
      const body = new URLSearchParams();
      body.set('username', username);
      body.set('password', password);
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.detail || '登录失败');
      }
      setSession(data.accessToken || data.access_token, data.user);
      push('/');
    } catch (e) {
      error = e.message || String(e);
    } finally {
      loading = false;
    }
  }
</script>

<div class="login-wrap">
  <div class="card panel">
    <div class="mark">靛</div>
    <h1>LoomLot 染坊台</h1>
    <p>靛蓝缸染 · 染程与色牢度抽检</p>
    <form on:submit|preventDefault={submit}>
      <label>
        用户名
        <input bind:value={username} autocomplete="username" />
      </label>
      <label>
        密码
        <input type="password" bind:value={password} autocomplete="current-password" />
      </label>
      {#if error}
        <p class="err">{error}</p>
      {/if}
      <button class="btn" type="submit" disabled={loading}>
        {loading ? '登录中…' : '进入染坊'}
      </button>
    </form>
    <p class="hint">演示：admin / 123456（染坊主管）· dyer / 123456（染程操作员）</p>
  </div>
</div>

<style>
  .login-wrap {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 1.5rem;
  }

  .card {
    width: min(400px, 100%);
    text-align: center;
  }

  .mark {
    width: 56px;
    height: 56px;
    margin: 0 auto 0.75rem;
    display: grid;
    place-items: center;
    font-family: var(--font-display);
    font-size: 1.6rem;
    border-radius: 50% 45% 55% 50%;
    background: radial-gradient(circle at 30% 25%, #8b7cf0, var(--indigo-deep) 70%);
    border: 1px solid rgba(200, 192, 240, 0.35);
  }

  h1 {
    font-family: var(--font-display);
    font-size: 1.8rem;
    margin: 0 0 0.35rem;
    letter-spacing: 0.08em;
  }

  p {
    color: var(--indigo-mist);
    margin: 0 0 1.25rem;
    font-size: 0.9rem;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    text-align: left;
  }

  .btn {
    margin-top: 0.35rem;
    width: 100%;
  }

  .hint {
    margin-top: 1rem;
    font-size: 0.75rem;
  }
</style>
