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
        <a href="https://t.me/gatosdodois" target="_blank" class="text-accent">comunidade</a> primeiro!
        </p>
      <label class="label" for="cdm_path">
        <span class="label-text mb-2">
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
    </div>
    `,
  }