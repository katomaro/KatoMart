export default {
  props: {
    title: String,
    content: Object || String,
    type: {
      type: String,
      default: "arrow"
    },
  },


  template: `
  <div :class="['collapse', 'collapse-' + type, 'bg-base-200']">
    <input type="checkbox" class="peer" />
    <div class="collapse-title pl-0.5 py-0.5">
      <div v-html="title"></div>
    </div>
    <div class="collapse-content">
      <slot></slot>
    </div>
  </div>
  `

}