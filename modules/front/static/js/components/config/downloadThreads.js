export default {
  props: {
    modelValue: String,
  },
  methods: {
    updateValue(event) {
      this.$emit("update:modelValue", event.target.value);
    }
  },
  template: `
  <div class="bg-base-200 rounded-lg">
    <label class="label" for="download_threads">
      <span class="label-text mb-2">
        <i class="fas fa-project-diagram mr-1"></i>
        <span class="font-semibold">Quantidade de threads (Conexões Simultâneas):</span>
      </span>
      <span
        v-if="modelValue > 4"
        class="label-text-alt text-xs text-warning">Usar mais que 4 threads pode acarretar em banimento da conta.
      </span>
    </label>
    <input
      type="number"
      min="1"
      max="32"
      step="1"
      class="input input-bordered input-xs w-full bg-base-200"
      id="download_threads"
      name="download_threads"
      :value="modelValue"
      @input="updateValue"
    />
  </div>
  `
}
