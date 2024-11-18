export default {
  data() {
    return {
      platforms: []
    }
  },
  async mounted() {
    this.platforms = await fetch('/api/platforms').then(res => res.json())
  },
  template: `
  <div class="join flex justify-center mt-3">
    <input class="input input-bordered input-sm join-item" placeholder="Pesquisar Cursos" />

    <select class="select select-bordered select-sm join-item">
      <option disabled selected>Plataforma</option>
      <option v-for="platform in platforms" :value="platform[0]">{{ platform[1] }}</option>
    </select>

    <select class="select select-bordered select-sm join-item">
      <option disabled selected>Status</option>
      <option>Baixando</option>
      <option>Completo</option>
      <option>Não Iniciado</option>
      <option>Erro</option>
    </select>
  </div>
  `
}