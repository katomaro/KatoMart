import { toBRL } from "../../../utils.js"

export default {
  props: {
    sponsors: Array
  },
  setup() {
    return { toBRL }
  },
  template: `
  <h3 class="text-2xl font-bold mb-8">Sponsors do projeto</h3>
  <p class="mt-4 mb-4">Agradeça as pessoas listadas abaixo, pois ela ssão responsáveis por pelos menos 40% do projeto!
      <strong>Elas também recebem suporte 1:1 e terão acesso à algumas coisas extras no futuro por sua boa vontade</strong>
      (Coisas como toda a documentação que eu faço para mim mesmo, e que não é publicada, e acesso a versões de testes 
      antes de serem lançadas, etc.)
  </p>
  <table class="table w-full">
    <thead>
      <tr>
        <th>Doador</th>
        <th>Forma de Contribuição</th>
        <th>Valor</th>
        <th>Mensagem/Propaganda</th>
        <th>Data da Contribuição</th>
        <th>Referência da Transação</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="sponsor in sponsors">
        <td v-html="'<p>' + sponsor.contributor_name + '</p>'"></td>
        <td>{{ sponsor.contribution_resource }}</td>
        <td>{{ toBRL(parseFloat(sponsor.contribution_value)) }}</td>
        <td>{{ sponsor.contribution_message }}</td>
        <td>{{ sponsor.contribution_date }}</td>
        <td>{{ sponsor.contribution_reference_id }}</td>
      </tr>
    </tbody>
  </table>
  `
}