import { toBRL } from "../../../utils.js"

export default {
  props: {
    expenses: Array,
  },
  setup() {
    return {
      toBRL
    }
  },
  template: `
  <h3 class="text-2xl font-bold mb-8 mt-8">Gastos com o projeto</h3>
  <p class="mt-4 mb-4">Estes gastos podem ser tanto por motivos JURÍDICOS, ou, acesso à plataformas 
    para que elas possam ser implementadas no projeto.
  </p>
  <table class="table w-full" id="tabela-expenses">
    <thead>
      <tr>
          <th>Desenvolvedor Responsável</th>
          <th>Tipo de gasto</th>
          <th>Valor Gasto</th>
          <th>Motivo</th>
          <th>Data do Gasto</th>
          <th>Referência da Transação</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="expense in expenses">
        <td v-html="expense.developer"></td>
        <td>{{ expense.expense_type }}</td>
        <td>{{ toBRL(expense.expent_amount) }}</td>
        <td>{{ expense.expense_reason }}</td>
        <td>{{ expense.expense_date }}</td>
        <td>{{ expense.contribution_reference_id }}</td>
      </tr>
    </tbody>
  </table>
  `
}