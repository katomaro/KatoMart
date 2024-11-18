export default {
  props: {
    modelValue: Object,
    total: Number,
  },
  emits: ["update:modelValue"],
  computed: {
    totalPages() {
      return Math.ceil(this.total / this.modelValue.perPage)
    },
    nextPage() {
      return this.modelValue.page + 1 <= this.totalPages ? this.modelValue.page + 1 : null
    },
    prevPage() {
      return this.modelValue.page - 1 >= 1 ? this.modelValue.page - 1 : null
    },
    currentPage() {
      return this.modelValue.page
    }
  },
  methods: {
    loadPage(page) {
      this.$emit("update:modelValue", { ...this.modelValue, page })
    },
  },
  template: `
  <div class="join flex justify-center mt-4" v-if="totalPages > 1">
    <!-- primeira página -->
    <button class="join-item btn" @click="loadPage(1)" v-if="currentPage !== 1">1</button>

    <!-- paginas anteriores -->
    <button class="join-item btn" :disabled="!prevPage && prevPage !== 1" @click="loadPage(prevPage)">‹</button>

    <!-- página atual -->
    <button class="join-item btn btn-primary" :disabled="modelValue.page === totalPages && currentPage !== totalPages" @click="loadPage(modelValue.page)">{{ modelValue.page }}</button>

    <!-- proximas paginas -->
    <button class="join-item btn" :disabled="!nextPage && nextPage !== totalPages" @click="loadPage(nextPage)">›</button>

    <!-- ultima página -->
    <button class="join-item btn" @click="loadPage(totalPages)" v-if="currentPage !== totalPages">{{ totalPages }}</button>
  </div>
  `
}