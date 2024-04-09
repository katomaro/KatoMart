import { DOWNLOAD_STATUS_COLOR_MAP } from "../../constants.js"
import Children from "./children.js"

export default {
  name: "CourseCard",
  props: {
    course: Object
  },
  components: {
    Children,
  },
  data() {
    return {
      DOWNLOAD_STATUS_COLOR_MAP
    }
  },
  template: `
  <div class="card w-full bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title flex justify-between">
        <span class="text-lg">{{ course.name }}</span>
        <div :class="'badge badge-' + DOWNLOAD_STATUS_COLOR_MAP[course.status]">
          {{ course.status }}
        </div>
      </h2>
      <div class="flex items-center gap-2">
        <progress
          class="progress progress-accent w-full"
          :value="course.progress * 100"
          max="100"
        />
        <p class="text-base">{{ course.progress * 100 }}%</p>
      </div>

      <Children v-if="course.children.length > 0" :children="course.children" />
    </div>
  </div>
  `
}