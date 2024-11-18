import downloads from "../components/logs/downloads.js"
import logs from "../components/logs/logs.js"

export default {
  components: {
    'Downloads': downloads,
    'Logs': logs
  },
  template: `
  <div class="flex flex-row justify-center mt-2 mb-24">
    <Downloads />
    <div class="divider divider-horizontal"></div>
    <Logs />
  </div>
  `
}