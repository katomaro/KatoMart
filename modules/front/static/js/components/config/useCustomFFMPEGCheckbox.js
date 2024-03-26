export default {
  props: {
    modelValue: Boolean
  },
  template: `
  <label class="cursor-pointer label">
    <span class="label-text mb-2">
      <i class="fas fa-video"></i>
      <span class="font-semibold">Usar FFMPEG Não acessível pelo terminal?</span>
    </span>
    <input
      type="checkbox"
      id="use_custom_ffmpeg"
      name="use_custom_ffmpeg"
      class="checkbox checkbox-primary checkbox-sm"
      :checked="modelValue"
      @change="$emit('update:modelValue', $event.target.checked)"
    />
  </label>
  `
}