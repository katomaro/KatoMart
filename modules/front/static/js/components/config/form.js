import Button from "../button.js"
import Collapsible from "../collapsible.js"
import Tooltip from "../tooltip.js"
import UseCustomFFMPEGCheckbox from "./useCustomFFMPEGCheckbox.js"
import CustomFFMPEGPathInput from "./customFFMPEGPathInput.js"
import downloadWidevineCheckbox from "./downloadWidevineCheckbox.js"
import CDMPathInput from "./CDMPathInput.js"
import DefaultUserAgentInput from "./defaultUserAgentInput.js"
import DownloadPathInput from "./downloadPathInput.js"
import DRMTypesCheckbox from "./drmTypesCheckbox.js"
import MediaTypeCheckbox from "./mediaTypeCheckbox.js"


const { ref, onMounted } = Vue

export default {
  components: {
    Button,
    Tooltip,
    Collapsible,
    DRMTypesCheckbox,
    UseCustomFFMPEGCheckbox,
    CustomFFMPEGPathInput,
    'download-widevine-checkbox': downloadWidevineCheckbox,
    CDMPathInput,
    DownloadPathInput,
    MediaTypeCheckbox,
    DefaultUserAgentInput,
  },
  setup() {
    const settings = ref({})
    const isLoading = ref(true)
    const message = ref("")

    async function getSettingsData() {
      const res = await fetch('/api/settings')
      const data = await res.json()
      return data
    }

    onMounted(async () => {
      const data = await getSettingsData()
      settings.value = data.settings
      isLoading.value = false
    })

    async function handleSubmit() {
      const res = await fetch('/api/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings.value)
      })

      if (res.ok) {
        const data = await res.json()
        message.value = data.message
      }
    }

    return { settings, isLoading, handleSubmit, message }
  },
  template: `
  <div v-if="isLoading">
    <p>Carregando...</p>
  </div>

  <form v-else class="grid grid-cols-1 gap-4 mb-32" @submit.prevent="handleSubmit">
    <div v-if="message">
      <p class="alert alert-info flex justify-between">
        {{ message }}
        <button class="btn btn-outline btn-error btn-sm" @click="message = ''">Fechar</button>
      </p>
    </div>

    <DownloadPathInput v-model="settings.download_path" />

    <DefaultUserAgentInput v-model="settings.default_user_agent" />

    <download-widevine-checkbox v-model="settings.download_widevine" />

    <CDMPathInput v-if="settings.download_widevine" v-model="settings.widevine_cdm_path" />

    <UseCustomFFMPEGCheckbox v-model="settings.use_custom_ffmpeg" />

    <CustomFFMPEGPathInput v-if="settings.use_custom_ffmpeg" v-model="settings.custom_ffmpeg_path" />

    <Collapsible
      title='<i class="fa-solid fa-download"></i>
      <span class="font-semibold text-base">Tipo de Conteúdo a ser baixado</span>'
    >
      <div className="grid grid-cols-3 gap-2">
        <MediaTypeCheckbox
          v-for="{name, description, download} in Object.values(settings.media_types)"
          :name="name"
          :description="description"
          :value="download"
          :onChange="() => settings.media_types.find(x => x.name === name).download = !settings.media_types.find(x => x.name === name).download"
        />
      </div>
    </Collapsible>

    <Collapsible
      title='<i class="fas fa-lock"></i>
      <span class="font-semibold text-base">
        Tipo de DRM a ser baixado
      </span>'
    >
      <div className="grid grid-cols-3 gap-2">
        <DRMTypesCheckbox
          v-for="{name, description, download} in Object.values(settings.drm_types)"
          :name="name"
          :description="description"
          :value="download"
          :onChange="() => settings.drm_types.find(x => x.name === name).download = !settings.drm_types.find(x => x.name === name).download"
        />
      </div>
    </Collapsible>


    <Button type="submit" outline>Atualizar configurações</Button>
  </form>
  `
}
