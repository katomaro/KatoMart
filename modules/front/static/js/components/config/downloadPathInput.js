import Tooltip from "../tooltip.js";

export default {
  props: {
    modelValue: String,
  },
  components: {
    Tooltip,
  },
  methods: {
    updateValue(event) {
      this.$emit("update:modelValue", event.target.value);
    }
  },
  template: `
  <div class="bg-base-200 rounded-lg">
    <label class="label" for="download_path">
      <span class="label-text mb-2">
        <Tooltip tip='Por padrão ele salva na pasta do script dentro de uma pasta chamada "Cursos"'>
          <i class="fas fa-folder-open mr-1"></i>
          <span class="font-semibold">Caminho completo para salvar os cursos:</span>
        </Tooltip>
      </span>
    </label>
    <input
      type="text"
      class="input input-bordered input-xs w-full bg-base-200"
      id="download_path"
      name="download_path"
      :value="modelValue"
      @input="updateValue"
    />
  </div>
  `
}
