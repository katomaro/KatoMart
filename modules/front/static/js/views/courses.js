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
      await fetch("/api/start_download", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ courses: courses.value })
      })
      router.push("/logs")
    }


    return {
      courses,
      search,
      filteredCourses,
      startDownload,
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

    <div class="flex justify-center items-center gap-2 text-xl" v-if="isLoading">
      <i class="fa-solid fa-spinner animate-spin"></i>
      Cerregando cursos... (caso tenha muitos cursos, isso pode demorar um pouco.)
    </div>

    <div class="grid grid-cols-2 gap-4 justify-items-center">
      <CourseItem v-for="course in filteredCourses" :key="course.data.name" :course="course" />
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
