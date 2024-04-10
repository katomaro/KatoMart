export default {
  props: {
    query: Object,
  },
  template: `
  <div class="join flex justify-center mt-3">
    <input class="input input-bordered input-sm join-item" placeholder="Data Inicial" />

    <input class="input input-bordered input-sm join-item" placeholder="Data Final" />

    <select class="select select-bordered select-sm join-item">
      <option value="debug">Debug</option>
      <option value="info">Info</option>
      <option value="warn">Warning</option>
      <option value="error">Error</option>
      <option value="critical">Critical</option>
    </select>
  </div>
  `
}
