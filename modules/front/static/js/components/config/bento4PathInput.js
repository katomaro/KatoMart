export default {
  props: {
    modelValue: String
  },
  template: `
  <div>
    <label class="label" for="cdm_path">
      <span class="label-text mb-2">
        Caminho COMPLETO para A PASTA dos binários do
        <a href="https://www.bento4.com/downloads/" target="_blank" class="text-accent hover:underline">Bento4 Toolbox</a>
        (não apontar nenhum arquivo, apenas a pasta terminada em /):
      </span>
    </label>
    <input
      type="text"
      id="bento4_toolbox_path"
      name="bento4_toolbox_path"
      :value="modelValue"
      class="input input-bordered input-xs w-full"
      @input="$emit('update:modelValue', $event.target.value || 'SYSTEM')"
    />
    <label class="label">
      <span class="label-text-alt"></span>
      <span class="label-text-alt">
        AVISO: Use <span class="text-secondary">SYSTEM</span> caso esteja nas variáveis de ambiente.
      </span>
    </label>
  </div>
  `,
}