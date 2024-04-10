
import { LOGS_PLACEHOLDER_EXAMPLE } from "../../constants.js";
import LogsContent from "./logs-content.js";
import LogsFilter from "./logs-filter.js";
import LogsPagination from "./logs-pagination.js";

export default {
  components: {
    LogsFilter,
    LogsContent,
    LogsPagination
  },
  data() {
    const logsData = {
      total: 0,
      logs: []
    }
    const logsQuery = {
      level: "warn",
      perPage: 15,
      page: 1,
      startDate: "",
      endDate: ""
    };

    return { logsData, logsQuery, intervalId: null }
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
    <LogsFilter :query="logsQuery" />
    <LogsContent :logs="logsData.logs" />
    <LogsPagination
      :total="logsData.total"
      v-model="logsQuery"
    />
  </div>
  `
}