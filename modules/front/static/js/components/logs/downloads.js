import { COURSES_PLACEHOLDER_EXAMPLE } from "../../constants.js"
import courseCard from "./course-card.js"
import searchBar from "./search-bar.js"
import totalProgress from "./total-progress.js"

export default {
  components: {
    "SearchBar": searchBar,
    "TotalProgress": totalProgress,
    "CourseCard": courseCard
  },
  data() {
    return { courses: [], intervalId: null, error: null }
  },
  methods: {
    clearInterval() {
      if (this.intervalId) {
        clearInterval(this.intervalId)
      }
    },
    async fetchData() {
      const res = await fetch("/api/courses_progress")
      if (res.ok) {
        try {
          const data = await res.json()
          if (data.message) {
            this.clearInterval()
            this.error = data.message
            return
          }
          this.courses = await res.json()
        } catch {
          this.courses = COURSES_PLACEHOLDER_EXAMPLE
        }
      } else {
        this.courses = COURSES_PLACEHOLDER_EXAMPLE
      }
    }
  },
  async mounted() {
    await this.fetchData()
    this.intervalId = setInterval(this.fetchData, 7500)
  },
  beforeUnmount() {
    this.clearInterval()
  },
  template: `
  <div class="w-full">
    <h1 class="text-2xl text-center font-bold">Downloads</h1>

    <SearchBar />
    <TotalProgress :courses="courses" />

    <div class="flex justify-center mt-4">
      <div v-if="error" class="alert alert-error shadow-lg text-center font-bold text-lg mb-6 w-1/2">
        {{ error }}
      </div>
    </div>

    <div className="flex flex-col gap-3">
      <CourseCard v-for="course in courses" :key="course.id" :course="course" />
    </div>
  </div>
  `
}