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
    return { courses: [], intervalId: null }
  },
  methods: {
    async fetchData() {
      const res = await fetch("/api/courses_progress")
      if (res.ok) {
        try {
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
    if (this.intervalId) {
      clearInterval(this.intervalId)
    }
  },
  template: `
  <div class="w-full">
    <h1 class="text-2xl text-center font-bold">Downloads</h1>

    <SearchBar />
    <TotalProgress :courses="courses" />

    <div className="flex flex-col gap-3">
      <CourseCard v-for="course in courses" :key="course.id" :course="course" />
    </div>
  </div>
  `
}