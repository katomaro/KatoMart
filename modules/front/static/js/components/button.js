export default {
  props: {
    variant: {
      type: String,
      default: "primary",
    },
    size: {
      type: String,
      default: "md",
    }
  },

  computed: {
    buttonClasses() {
      const variantClasses = {
        primary: "btn-primary",
        secondary: "btn-secondary",
        accent: "btn-accent",
      }
      const sizeClasses = {
        sm: "btn-sm",
        md: "btn-md",
        lg: "btn-lg",
      }

      return `btn ${variantClasses[this.variant]} ${sizeClasses[this.size]}`
    }
  },

  template: `
  <button :class="buttonClasses">
    <slot></slot>
  </button>
  `
}