<script>
  import { link, location } from 'svelte-spa-router';
  import { user, clearSession } from '../lib/auth.js';
  import { push } from 'svelte-spa-router';

  export let steps = [
    { path: '/houses', label: '染坊', hint: '水源与坊务' },
    { path: '/vats', label: '染缸', hint: '纤维与容量' },
    { path: '/lots', label: '染程', hint: '配方开缸' },
    { path: '/checks', label: '色牢度', hint: '抽检回写' },
  ];

  function logout() {
    clearSession();
    push('/login');
  }

  $: activeIdx = Math.max(
    0,
    steps.findIndex((s) => $location.startsWith(s.path))
  );
</script>

<header class="top">
  <div class="brand-row">
    <div class="brand">
      <span class="mark">靛</span>
      <div>
        <div class="name">LoomLot</div>
        <div class="tag">靛蓝染坊 · 缸染工艺台</div>
      </div>
    </div>
    <div class="who">
      <a href="/" use:link class="dash-link" class:on={$location === '/'}>总览</a>
      <span class="sep">·</span>
      <span>{$user?.displayName || $user?.username || ''}</span>
      <button class="btn ghost small" type="button" on:click={logout}>退出</button>
    </div>
  </div>

  <nav class="process" aria-label="工艺步骤">
    {#each steps as step, i}
      <a
        href={step.path}
        use:link
        class="step"
        class:active={$location.startsWith(step.path)}
        class:done={i < activeIdx}
      >
        <span class="idx">{i + 1}</span>
        <span class="meta">
          <span class="label">{step.label}</span>
          <span class="hint">{step.hint}</span>
        </span>
      </a>
      {#if i < steps.length - 1}
        <div class="rail" class:lit={i < activeIdx}></div>
      {/if}
    {/each}
  </nav>
</header>

<style>
  .top {
    padding: 1.1rem 1.5rem 0.85rem;
    border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(42, 26, 94, 0.92), rgba(26, 15, 60, 0.55));
  }

  .brand-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.1rem;
  }

  .brand {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }

  .mark {
    width: 44px;
    height: 44px;
    display: grid;
    place-items: center;
    font-family: var(--font-display);
    font-size: 1.35rem;
    background: radial-gradient(circle at 30% 25%, #8b7cf0, var(--indigo-deep) 70%);
    border: 1px solid rgba(200, 192, 240, 0.35);
    border-radius: 50% 45% 55% 50%;
  }

  .name {
    font-family: var(--font-display);
    font-size: 1.45rem;
    letter-spacing: 0.12em;
  }

  .tag {
    font-size: 0.75rem;
    color: var(--indigo-mist);
    margin-top: 0.1rem;
  }

  .who {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 0.85rem;
    color: var(--indigo-mist);
  }

  .dash-link {
    opacity: 0.75;
  }

  .dash-link.on,
  .dash-link:hover {
    opacity: 1;
    color: white;
  }

  .sep {
    opacity: 0.4;
  }

  .process {
    display: flex;
    align-items: stretch;
    gap: 0;
    overflow-x: auto;
    padding-bottom: 0.35rem;
  }

  .step {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    min-width: 140px;
    padding: 0.7rem 0.9rem;
    border: 1px solid transparent;
    border-radius: 3px;
    color: var(--indigo-mist);
    transition: 0.15s ease;
  }

  .step:hover {
    background: rgba(107, 92, 231, 0.12);
    color: white;
  }

  .step.active {
    background: linear-gradient(120deg, rgba(107, 92, 231, 0.35), rgba(61, 42, 122, 0.4));
    border-color: rgba(107, 92, 231, 0.55);
    color: white;
  }

  .step.done .idx {
    background: rgba(76, 175, 130, 0.25);
    border-color: rgba(76, 175, 130, 0.5);
    color: var(--ok);
  }

  .idx {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 0.8rem;
    border: 1px solid var(--line);
    flex-shrink: 0;
  }

  .step.active .idx {
    background: var(--indigo-bright);
    border-color: var(--indigo-bright);
    color: white;
  }

  .meta {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
  }

  .label {
    font-weight: 500;
    letter-spacing: 0.04em;
  }

  .hint {
    font-size: 0.7rem;
    opacity: 0.75;
  }

  .rail {
    width: 28px;
    align-self: center;
    height: 2px;
    background: var(--line);
    flex-shrink: 0;
  }

  .rail.lit {
    background: linear-gradient(90deg, rgba(76, 175, 130, 0.7), rgba(107, 92, 231, 0.7));
  }

  @media (max-width: 720px) {
    .brand-row {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>
