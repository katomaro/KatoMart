import Tooltip from "../tooltip.js"

export default {
  components: {
    Tooltip
  },
  props: {
    modelValue: String
  },
  template: `
  <div class="bg-base-200 rounded-lg">
    <label class="label" for="default_user_agent">
      <span class="label-text mb-2">
        <Tooltip tip="Não alterar se não souber o que estiver fazendo">
          <i class="fas fa-user-secret"></i>
          <span class="font-semibold">
            Navegador Simulado (<span class="text-accent italic">User-Agent</span>):
          </span>
        </Tooltip>
      </span>
    </label>
    <input
      type="text"
      id="default_user_agent"
      name="default_user_agent"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="input input-bordered input-xs w-full bg-base-200"
    />
  </div>
  `
}