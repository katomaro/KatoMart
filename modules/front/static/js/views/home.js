import notices from "../components/home/notices.js"
import presentation from "../components/home/presentation.js"

export default {
  components: {
    presentation,
    notices
  },


  template: `
  <div class="container mx-auto">
    <presentation />
    <notices />
  </div>
  `
}