export default {
  props: {
    variant: {
      type: String,
      default: "primary",
    },
    size: {
      type: String,
      default: "md",
    },
    outline: {
      type: Boolean,
      default: false,
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

      return `btn ${variantClasses[this.variant]} ${sizeClasses[this.size]} ${this.outline ? "btn-outline" : ""}`
    }
  },

  template: `
  <button :class="buttonClasses">
    <slot></slot>
  </button>
  `
}