const { useRouter } = VueRouter
const { ref } = Vue

export default {
  setup() {
    const pages = [
      {
        name: "Termos de Uso",
        icon: "fa-solid fa-circle-exclamation",
        link: "/agreement"
      },
      {
        name: "Katomart",
        icon: "fa-solid fa-house",
        link: "/"
      },
      {
        name: "Configurações",
        icon: "fa-solid fa-sliders",
        link: "/config"
      },
      {
        name: "Contas",
        icon: "fa-solid fa-users",
        link: "/accounts"
      },
      {
        name: "Cursos",
        icon: "fa-solid fa-cloud-arrow-down",
        link: "/courses"
      },
      {
        name: "LOGs",
        icon: "fa-solid fa-file-lines",
        link: "/logs"
      },
      {
        name: "Suporte",
        icon: "fa-solid fa-paper-plane",
        link: "/support"
      }
    ]
    const currentRoutePath = ref("")
    return { pages, currentRoutePath }
  },
  mounted() {
    this.currentRoutePath = useRouter().currentRoute.value.path
  },
  template: `
  <nav class="navbar py-2 bg-base-100 shadow-lg rounded-b-lg flex justify-around">
    <RouterLink
      v-for="page in pages"
      :key="page.name"
      :class="currentRoutePath.includes(page.link) ? 'btn btn-accent' : 'btn btn-primary'"
      :to="page.link"
    >
      <i :class="page.icon"></i> {{ page.name }}
    </RouterLink>
  </nav>
  `
}