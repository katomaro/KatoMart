import { stringToDateTime } from "../../utils.js"

export default {
  props: {
    logs: Array
  },
  data() {
    return {
      stringToDateTime
    }
  },
  methods: {
    levelColor(level) {
      switch (level) {
        case 'error':
          return 'error'
        case 'warn':
          return 'warning'
        case 'info':
          return 'info'
        case 'debug':
          return 'success'
        default:
          return 'info'
      }
    }
  },
  template: `
  <div class="overflow-x-auto">
    <table class="table table-zebra">
      <thead class="text-center">
        <tr>
          <th>Data</th>
          <th>Mensagem</th>
          <th>Nível</th>
          <th>Dados Sensíveis?</th>
        </tr>
      </thead>
      <tbody class="text-center">
        <tr v-for="log in logs" :key="log.id">
          <th>{{ stringToDateTime(log.date) }}</th>
          <td>{{ log.message }}</td>
          <td>
            <span :class="['badge', 'badge-' + levelColor(log.level), 'uppercase']">
              {{ log.level }}
            </span>
          </td>
          <td>{{ log.sensitive ? 'Sim' : 'Não' }}</td>
        </tr>
      </tbody>
    </table>

    <p class="mt-4 mb-4" v-if="logs.length === 0">Nenhum log encontrado</p>

</div>
  `
}