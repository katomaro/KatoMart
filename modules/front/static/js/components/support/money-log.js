const { ref, onMounted } = Vue
import { CONTRIBUTIONS_URL, EXPENSES_URL } from "../../constants.js"
import MoneyBox from "./money-box.js"
import ExpensesTable from "./tables/expenses.js"
import SponsorsTable from "./tables/sponsors.js"

export default {
  components: { MoneyBox, SponsorsTable, ExpensesTable },
  async setup() {
    const sponsors = ref([])
    const expenses = ref([])

    onMounted(async () => {
      [sponsors.value, expenses.value] = await Promise.all([
        fetch(CONTRIBUTIONS_URL).then(res => res.json()),
        fetch(EXPENSES_URL).then(res => res.json())])
    })


    return {
      sponsors,
      expenses
    }
  },
  template: `
  <MoneyBox :sponsors="sponsors" :expenses="expenses" />
  <section class="mt-3 mb-28">
    <h1 class="text-3xl font-bold text-center mb-8 mt-8">
      <i class="fas fa-money-bill-transfer"></i> Fluxo / Saída da Caixinha
    </h1>
    <SponsorsTable :sponsors="sponsors" />
    <ExpensesTable :expenses="expenses" />
  </section>
  `
}