import { sanitizeString } from "../../utils.js"
import ModuleCollapsible from "./module-collapsible.js"

export default {
  components: { ModuleCollapsible },
  props: {
    course: Object,
    isModalOpen: Boolean,
  },
  data() {
    return {
      isOpen: this.isModalOpen,
      content: [],
      isLoading: true,
      search: "",
      sanitizeString
    }
  },
  watch: {
    isModalOpen() {
      this.isOpen = this.isModalOpen
      if (this.isOpen) {
        this.getContent()
      }
    }
  },
  emits: ['close-modal-request', 'set-course-modules'],
  methods: {
    closeModal() {
      this.isOpen = false
      this.$emit('close-modal-request')
    },
    getContent() {
      this.isLoading = true
      if (this.content.length) return this.isLoading = false
      fetch("/api/load_course_data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ club: this.course.data.subdomain }),
      })
        .then((res) => res.json())
        .then((data) => {
          this.content = data.modules.map(m => ({
            ...{

              ...m,
              name: sanitizeString(m.name),
              lessons: m.lessons.map(lesson =>
              ({
                ...lesson,
                selected: true,
                isEditLessonName: false,
                name: sanitizeString(lesson.name)
              }))

            },
            selected: true
          }))
          this.$emit('set-course-modules', this.content)
        })
        .finally(() => {
          this.isLoading = false
        })
    }
  },
  template: `
  <input type="checkbox" class="modal-toggle" v-model="isOpen" />
  <div class="modal" role="dialog">
    <div class="modal-box w-full max-w-7xl">
      <h3 class="font-bold text-2xl text-center my-4">Conteúdo do Curso {{ course.data.name }}</h3>

      <div v-if="isLoading" class="alert alert-info flex justify-center my-4">
        <i class="fa-solid fa-spinner animate-spin"></i> Carregando...
      </div>

      <div class="flex justify-center">
        <input
          class="input input-bordered input-sm w-3/4 mb-4"
          placeholder="Pesquisar Conteúdo"
          v-model="search"
          v-if="!isLoading"
        />
      </div>

      <div class="flex flex-col gap-2 max-h-[65vh] h-full overflow-y-auto">
        <ModuleCollapsible
          v-for="module in content.filter(module => module.name.toLowerCase().includes(search.toLowerCase()))"
          :module="module"
        />
      </div>

      <div class="modal-action justify-end">
        <button class="btn btn-error" @click="closeModal">
          <i class="fa-solid fa-xmark"></i> Fechar
        </button>
      </div>
    </div>
  </div>
  `
}