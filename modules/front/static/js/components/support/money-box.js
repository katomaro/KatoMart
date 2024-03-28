import { toBRL } from "../../utils.js"

export default {
  props: {
    sponsors: Array,
    expenses: Array,
  },
  setup() {

    return {
      toBRL
    }
  },
  computed: {
    totalExpenses() {
      return this.expenses.reduce((total, expense) => total + expense.expent_amount, 0)
    },
    totalSponsors() {
      return this.sponsors.reduce((total, sponsor) => total + parseFloat(sponsor.contribution_value), 0)
    },
    saldo() {
      return this.totalSponsors - this.totalExpenses
    }
  },
  template: `
  <section>
    <h1 class="text-3xl font-bold text-center mb-8">
      <i class="fas fa-sack-dollar"></i> Caixinha do Katomart:
      <span id="saldo-final">{{ toBRL(saldo) }}</span>
    </h1>
    <p class="text-center"> Este valor é utilizado para
      custear o desenvolvimento da aplicação como todo, e também manter seu repositório acessível
      ao público geral. Os lançamentos são feitos de forma manual no repositório do Katomart,
      e são atualizados sempre que você acessar esta página (pode acontecer um atraso para a atualização).
    </p>
  </section>
`
}