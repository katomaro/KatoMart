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
  <div>
    <label class="label" for="download_path">
      <span class="label-text mb-2">
        <Tooltip tip='Por padrão ele salva na pasta do script dentro de uma pasta chamada "Cursos"'>
          <i class="fas fa-folder-open"></i>
          <span class="font-semibold">Caminho completo para salvar os cursos:</span>
        </Tooltip>
      </span>
    </label>
    <input
      type="text"
      class="input input-bordered input-xs w-full"
      id="download_path"
      name="download_path"
      :value="modelValue"
      @input="updateValue"
    />
  </div>
  `
}
