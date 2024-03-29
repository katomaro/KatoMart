export default {
    props: {
      modelValue: Boolean
    },
    template: `
    <label class="cursor-pointer label">
      <span class="label-text mb-2">
      <i class="fa-solid fa-lock-open"></i>
        <span class="font-semibold">Baixar mídias bloqueadas pelo Widevine? <span style="color: red;">REQUER CDM (caminho completo)</span></span>
      </span>
      <input
        type="checkbox"
        id="download_widevine"
        name="download_widevine"
        class="checkbox checkbox-primary checkbox-sm"
        :checked="modelValue"
        @change="$emit('update:modelValue', $event.target.checked)"
      />
    </label>
    `
  }