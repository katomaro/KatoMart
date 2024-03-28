export default {
  props: {
    tip: {
      type: String,
      default: "",
    },
    color: {
      type: String,
      default: "primary",
    },
  },
  template: `
  <div :class="['tooltip', 'tooltip-' + color, 'tooltip-right', 'z-50']" :data-tip="tip">
    <slot></slot>
  </div>
  `
}