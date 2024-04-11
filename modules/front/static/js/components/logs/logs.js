
import { LOGS_PLACEHOLDER_EXAMPLE } from "../../constants.js";
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
          this.logsData = LOGS_PLACEHOLDER_EXAMPLE
        }
      } else {
        this.logsData = LOGS_PLACEHOLDER_EXAMPLE
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
    <h1 class="text-2xl text-center font-bold">LOGs</h1>
    <LogsContent :logs="logsData" />
    <LogsPagination
      :total="logsData.lenght"
      v-model="logsQuery"
    />

    <ExportLogsModal :query="logsQuery" />
  </div>
  `
}