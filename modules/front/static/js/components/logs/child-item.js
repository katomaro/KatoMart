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
  computed: {
    isFile() {
      return this.child.type !== undefined
    },
    status() {
      const progress = this.child.progress
      if (progress === 0) {
        return "Não Iniciado"
      } else if (progress === 1) {
        return "Completo"
      } else {
        return "Baixando"
      }
    },
  },
  template: `
  <h2 class="flex justify-between">
    <span class="text-lg">{{ child.name }}</span>
    <div class="flex gap-1 items-center">
      <span
        v-if="isFile"
        class="badge badge-info text-xs px-0.5">
          {{ child.type }}
      </span>
      <div
        class="radial-progress text-primary text-sm"
        :style="{ '--value': child.progress * 100, '--size': '3rem' }"
        role="progressbar"
      >
        {{ child.progress * 100 }}%
      </div>
      <div :class="'badge badge-' + DOWNLOAD_STATUS_COLOR_MAP[status]">
        {{ status }}
      </div>
    </div>
  </h2>
  `
}