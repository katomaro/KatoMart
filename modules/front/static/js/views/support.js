import Devs from "../components/support/devs.js"
import Info from "../components/support/info.js"
import MoneyLog from "../components/support/money-log.js"

export default {
  components: {
    MoneyLog,
    Info,
    Devs,
  },
  template: `
  <Info />
  <Devs />
  <div className="container mx-auto">
    <MoneyLog />
  </div>
  `
}