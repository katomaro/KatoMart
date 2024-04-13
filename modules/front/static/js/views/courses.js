const { onMounted, ref, watch } = Vue
const { useRouter } = VueRouter
import CourseItem from '../components/courses/course-item.js'

export default {
  components: {
    CourseItem,
  },
  setup() {
    const courses = ref([])
    const search = ref('')
    const isLoading = ref(true)
    const filteredCourses = ref([])
    const router = useRouter()

    const filterCourses = () => {
      filteredCourses.value = courses.value.filter(course =>
        course.data.name.toLowerCase().includes(search.value.toLowerCase()))
    }

    watch(search, () => {
      filterCourses()
    })

    const loadCourses = async () => {
      isLoading.value = true
      const response = await fetch('/api/courses')
      if (!response.ok) return router.push('/accounts')

      const data = await response.json()
      courses.value = data.courses.map(course => ({ ...course, selected: false }))
      filterCourses()
      isLoading.value = false
    }

    onMounted(loadCourses)

    const startDownload = async () => {
      devWarning.value = true
      await fetch("/api/start_download", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ courses: courses.value })
      })
    }

    const devWarning = ref(false)

    return {
      courses,
      search,
      filteredCourses,
      startDownload,
      devWarning,
      router,
      isLoading
    }
  },
  template: `
    <h1 class="text-2xl font-bold text-center mb-8">Download de Cursos</h1>
    <div class="flex flex-col items-center mb-2 gap-4">
      <input
        class="input input-bordered input-sm w-1/2"
        placeholder="Pesquise pelo Curso"
        v-model="search"
      />
      <div class="alert alert-warning w-1/2" role="alert" v-if="filteredCourses.length === 0 && !isLoading">
        Sem resultados para o termo '{{ search }}'
      </div>
    </div>
    <div class="grid grid-cols-2 gap-4 justify-items-center">
      <CourseItem v-for="course in filteredCourses" :key="course.data.name" :course="course" />
    </div>

    <input type="checkbox" class="modal-toggle" v-model="devWarning" />
    <div class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-lg">Atenção</h3>
        <p class="py-4 text-warning">
          Opa, o programa ainda está em desenvolvimento, isto significa que a
          opção de download <strong class="text-error font-bold text-lg">NÃO</strong> está disponível ainda.
        </p>
        <div class="modal-action">
          <button class="btn btn-secondary" @click="router.push('/')">Ir para a Home</button>
        </div>
      </div>
    </div>

    <div class="flex justify-center mt-4">
      <button
        v-if="courses.some(x => x.selected)"
        class="btn btn-accent"
        @click="startDownload()">
          <i class="fa-solid fa-download"></i>
          Baixar Selecionados ({{ courses.filter(x => x.selected).length }})
      </button>
    </div>
  `,
}
