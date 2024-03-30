export default {
  props: {
    modelValue: Boolean
  },
  template: `
  <label class="cursor-pointer label bg-base-200 rounded-lg">
    <span class="label-text mb-2">
      <i class="fas fa-video mr-1"></i>
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