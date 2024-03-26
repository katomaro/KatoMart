import Footer from "../components/footer.js"
import NavBar from "../components/navbar.js"

export default {
  components: {
    NavBar,
    Footer
  },
  template: `
  <NavBar />

  <div className="mb-24">
    <RouterView />
  </div>

  <Footer />
  `
}