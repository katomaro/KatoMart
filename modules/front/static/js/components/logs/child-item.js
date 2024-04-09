import { DOWNLOAD_STATUS_COLOR_MAP } from "../../constants.js"

export default {
  props: {
    child: Object
  },
  data() {
    return {
      DOWNLOAD_STATUS_COLOR_MAP
    }
  },
  template: `
  <h2 class="flex justify-between">
    <span class="text-lg">{{ child.name }}</span>
    <div class="flex gap-1 items-center">
      <span
        v-if="child.downloadedThings"
        v-for="thing in child.downloadedThings"
        class="badge badge-info text-xs px-0.5">
          {{ thing }}
      </span>
      <div :class="'badge badge-' + DOWNLOAD_STATUS_COLOR_MAP[child.status]">
        {{ child.status }}
      </div>
    </div>
  </h2>
  <div class="flex items-center gap-2">
    <progress
      class="progress progress-accent w-full"
      :value="child.progress * 100"
      max="100"
    />
    <p class="text-base">{{ child.progress * 100 }}%</p>
  </div>
  `
}