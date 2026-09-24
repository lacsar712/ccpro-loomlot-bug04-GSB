<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let rows = [];
  let error = '';
  let form = { name: '', waterNote: '', notes: '' };
  let editing = null;

  async function load() {
    error = '';
    try {
      rows = await api('/dye-houses');
    } catch (e) {
      error = e.message;
    }
  }

  onMount(load);

  async function save() {
    error = '';
    try {
      const body = {
        name: form.name.trim(),
        waterNote: form.waterNote.trim(),
        notes: form.notes.trim() || null,
      };
      if (editing) {
        await api(`/dye-houses/${editing}`, { method: 'PUT', body: JSON.stringify(body) });
      } else {
        await api('/dye-houses', { method: 'POST', body: JSON.stringify(body) });
      }
      form = { name: '', waterNote: '', notes: '' };
      editing = null;
      await load();
    } catch (e) {
      error = e.message;
    }
  }

  function startEdit(row) {
    editing = row.id;
    form = {
      name: row.name,
      waterNote: row.waterNote,
      notes: row.notes || '',
    };
  }

  async function remove(id) {
    if (!confirm('确认删除该染坊？')) return;
    error = '';
    try {
      await api(`/dye-houses/${id}`, { method: 'DELETE' });
      await load();
    } catch (e) {
      error = e.message;
    }
  }
</script>

<h1 class="page-title">染坊</h1>
<p class="page-sub">维护坊名、用水说明与备注。</p>

<div class="panel" style="margin-bottom:1rem;">
  <div class="form-grid">
    <label>名称 <input bind:value={form.name} /></label>
    <label>用水说明 <input bind:value={form.waterNote} /></label>
    <label>备注 <input bind:value={form.notes} /></label>
  </div>
  <div class="toolbar">
    <button class="btn" type="button" on:click={save}>{editing ? '保存修改' : '新建染坊'}</button>
    {#if editing}
      <button
        class="btn ghost"
        type="button"
        on:click={() => {
          editing = null;
          form = { name: '', waterNote: '', notes: '' };
        }}>取消</button
      >
    {/if}
  </div>
  {#if error}<p class="err">{error}</p>{/if}
</div>

<div class="panel">
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>名称</th>
        <th>用水说明</th>
        <th>备注</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {#each rows as row}
        <tr>
          <td>{row.id}</td>
          <td>{row.name}</td>
          <td>{row.waterNote}</td>
          <td>{row.notes || '—'}</td>
          <td class="row-actions">
            <button class="btn ghost small" type="button" on:click={() => startEdit(row)}>编辑</button>
            <button class="btn danger small" type="button" on:click={() => remove(row.id)}>删除</button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
