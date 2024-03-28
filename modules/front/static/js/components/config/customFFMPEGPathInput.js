export default {
  props: {
    modelValue: String
  },
  template: `
  <div id="customFfmpegInput">
    <p class="mb-2">
      <span class="text-accent">"SYSTEM"</span> indica para usar o padrão do
      terminal, você não deveria ver esse campo se não alterou o anterior para
      verdadeiro.
    </p>
    <label class="label" for="custom_ffmpeg_path">
      <span class="label-text mb-2">
        Caminho COMPLETO para o ffmpe.exe (incluir ffmpeg.exe no final):
      </span>
    </label>
    <input
      type="text"
      id="custom_ffmpeg_path"
      name="custom_ffmpeg_path"
      :value="modelValue"
      class="input input-bordered input-xs w-full"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
  `,
}