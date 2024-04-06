export default {
  template: `
  <div class="join flex justify-center mt-3">
    <input class="input input-bordered input-sm join-item" placeholder="Pesquisar Cursos" />

    <select class="select select-bordered select-sm join-item">
      <option disabled selected>Plataforma</option>
      <option>Hotmart</option>
      <option>Kiwify</option>
      <option>Ainnn</option>
    </select>

    <select class="select select-bordered select-sm join-item">
      <option disabled selected>Status</option>
      <option>Baixando</option>
      <option>Completo</option>
    </select>
  </div>
  `
}