
export default {
  props: {
    courses: Array,
  },
  computed: {
    totalProgress() {
      if (!this.courses.length) return 0
      return this.courses.reduce((acc, cur) => acc + cur.progress, 0) / this.courses.length * 100
    }
  },
  template: `
  <div class="mt-4">
    <h2 class="text-sm text-center">Progresso Total</h2>
    <div class="flex justify-center gap-3 items-center">
      <progress
        class="progress progress-secondary w-3/4"
        :value="totalProgress"
        max="100"
      />
      <p class="text-base">{{ totalProgress }}%</p>
    </div>
  </div>
  `
}