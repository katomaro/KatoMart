import Footer from "../components/footer.js"
import NavBar from "../components/navbar.js"

export default {
  components: {
    NavBar,
    Footer
  },
  template: `
  <NavBar />

  <div class="mb-24">
    <Suspense>
      <RouterView />
    </Suspense>
  </div>

  <Footer />
  `
}