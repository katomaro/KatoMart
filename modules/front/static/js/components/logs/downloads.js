const { ref, onMounted } = Vue

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
  setup() {
    const courses = ref([])
    const logs = ref([])
    onMounted(async () => {
      // TODO: Call an API that will returns the courses progress :D
      // courses.value, logs.value = await Promise.all([
      //   fetch('/api/courses').then(res => res.json()),
      //   fetch('/api/logs').then(res => res.json())
      // ])

      // TODO: remove this placeholder when the API is ready
      courses.value = COURSES_PLACEHOLDER_EXAMPLE
    })
    return { courses, logs }
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