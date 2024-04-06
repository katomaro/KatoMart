import courseCard from "./course-card.js"
import searchBar from "./search-bar.js"
import totalProgress from "./total-progress.js"

export default {
  components: {
    "SearchBar": searchBar,
    "TotalProgress": totalProgress,
    "CourseCard": courseCard
  },
  template: `
  <div class="w-full">
    <h1 class="text-2xl text-center font-bold">Downloads</h1>

    <SearchBar />
    <TotalProgress />

    <CourseCard />
  </div>
  `
}