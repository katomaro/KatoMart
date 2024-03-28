const { ref, onMounted } = Vue
const { useRouter } = VueRouter
import CourseItem from "../components/courses/course-item.js"

export default {
  setup() {
    const courses = ref([])
    const router = useRouter()

    onMounted(async () => {
      const res = await fetch('/api/courses')
      if (!res.ok) {
        return router.push('/accounts')
      }
      const data = await res.json()
      courses.value = data.courses.map(c => ({ ...c, selected: false }))
    })

    return {
      courses,
    }
  },
  components: {
    CourseItem
  },
  template: `
  <h1 class="text-2xl font-bold text-center mb-8">Download de Cursos</h1>

  <div className="flex flex-col gap-4 justify-center items-center">
    <CourseItem v-for="course in courses" :key="course.id" :course="course" />
  </div>
  `
}