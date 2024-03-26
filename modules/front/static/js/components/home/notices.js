const { ref, onMounted } = Vue
import { GITHUB_NOTICE_URL } from "../../constants.js"

export default {
  setup() {
    const rawData = ref("")
    const loading = ref(true)

    async function getNotices() {
      try {
        const response = await fetch(GITHUB_NOTICE_URL)
        const data = await response.text()
        rawData.value = data
        loading.value = false
      } catch (error) {
        console.error(error)
        rawData.value = error
        loading.value = false
      }
    }

    onMounted(getNotices)

    return { rawData, loading }

  },
  template: `
  <section>
    <h3 class="alert mb-3" role="alert">
      <i class="fa-solid fa-triangle-exclamation"></i>
      Esta seção abaixo é utilizada para puxar mensagens que os desenvolvedores julgarem
      como importante, diretamente do repositório de código do programa.
    </h3>
    <div
      id="aviso"
      class="p-4 border-2 rounded-lg border-accent border-dotted overflow-y-auto h-screen"
    >
      <p class="alert alert-warning" role="alert" v-if="loading">
        <span class="loading loading-spinner loading-xs"></span>
        Carregando avisos...
      </p>
      <div v-else v-html="rawData"></div>
    </div>
  </section>
  `
}