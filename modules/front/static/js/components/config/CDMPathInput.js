export default {
  props: {
    modelValue: String
  },
  template: `
  <div id="CDMPathInput">
      <p class="mb-2">
      AVISO: Esta é uma configuração bem avançada, você não precisa para a 
      maioria dos downloads, se você precisa interagir com isso, se refira ao
      grupo da comunidade para ter acesso à guias e a ajuda. Você vai precisar.
      <a href="https://t.me/katomart" target="_blank" class="text-accent hover:underline">Link da Comuninidade</a>
      </p>
    <label class="label">
      <span class="label-text">
        Caminho COMPLETO para A PASTA da CDM a ser usada no Widevine (não apontar nenhum arquivo, apenas a pasta terminada em /):
      </span>
    </label>
    <input
      type="text"
      id="widevine_cdm_path"
      name="widevine_cdm_path"
      :value="modelValue"
      class="input input-bordered input-xs w-full"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <label class="label">
      <span class="label-text-alt"></span>
      <span class="label-text-alt text-warning">
        Evite utilizar CDM's genéricos, provavelmente não funcionarão. Para garantir funcionamento, extraia o CDM de um celular android.
      </span>
    </label>
  </div>
  `,
}