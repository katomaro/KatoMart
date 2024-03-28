import Tooltip from "../tooltip.js";

export default {
  props: {
    value: Boolean,
    name: String,
    description: String,
    onChange: Function
  },
  components: {
    Tooltip
  },
  template: `
  <label class="inline-flex items-center mb-1">
  <input
    type="checkbox"
    :id="name"
    :name="name"
    class="checkbox checkbox-primary checkbox-sm"
    :checked="value"
    @change="onChange()"
  />
  <Tooltip :tip="description">
    <span class="ml-2 hover:underline">
      Baixar <span class="text-secondary">{{ name }}</span>?
    </span>
  </Tooltip>
</label>
  `
}