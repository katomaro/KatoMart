export default {
  props: {
    modelValue: Boolean
  },
  template: `
  <label class="cursor-pointer label bg-base-200 rounded-lg">
    <span class="label-text mb-2 flex items-center">
      <i class="fas fa-info-circle mr-1"></i>
      <div class="tooltip flex items-center" data-tip="Nomes e Afins">
        <span class="font-semibold">
          Obter informações extras do produto.
          (<span class="text-error">Faz a listagem de produtos demorar mais.</span>)
        </span>
      </div>
    </span>
    <input
      type="checkbox"
      id="get_product_extra_info"
      name="get_product_extra_info"
      class="checkbox checkbox-primary checkbox-sm"
      :checked="modelValue"
      @change="$emit('update:modelValue', $event.target.checked)"
    />
  </label>
  `
}