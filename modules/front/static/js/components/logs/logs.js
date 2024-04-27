
import ExportLogsModal from "./export-logs-modal.js";
import LogsContent from "./logs-content.js";
import LogsPagination from "./logs-pagination.js";

export default {
  components: {
    LogsContent,
    LogsPagination,
    ExportLogsModal
  },
  data() {
    const logsData = []
    const logsQuery = {
      perPage: 15,
      page: 1,
    };

    return { logsData, logsQuery, intervalId: null, isModalOpen: false }
  },
  async mounted() {
    await this.loadLogsQuery()
    this.intervalId = setInterval(this.loadLogsQuery, 7500)
  },
  beforeUnmount() {
    if (this.intervalId) {
      clearInterval(this.intervalId)
    }
  },
  methods: {
    async loadLogsQuery() {
      const fLogsQuery = new URLSearchParams(this.logsQuery)
      const res = await fetch(`/api/logs?${fLogsQuery.toString()}`)
      if (res.ok) {
        try {
          const data = await res.json()
          this.logsData = data
        } catch {
          // TODO: handle error
        }
      } else {
        // TODO: handle error
      }
    }
  },
  watch: {
    logsQuery() {
      this.loadLogsQuery()
    }
  },
  template: `
  <div class="w-full">
    <h1 class="flex justify-center items-center gap-3 text-2xl font-bold">
      LOGs
      <ExportLogsModal :query="logsQuery" />
    </h1>
    <LogsContent :logs="logsData" />
    <LogsPagination
      :total="logsData.lenght"
      v-model="logsQuery"
    />
  </div>
  `
}