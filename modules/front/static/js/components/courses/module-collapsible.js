import ModuleContent from "./module-content.js"

export default {
  components: { ModuleContent },
  props: {
    module: Object
  },
  data() {
    return {
      isEditModuleName: false,
      showContent: false,
      searchContent: "",
    }
  },
  watch: {
    'module.selected'() {
      this.module.pages.forEach(lesson => {
        lesson.selected = this.module.selected
      })
    }
  },
  template: `
  <div class="card">
    <div class="card-body px-2 py-1 m-0.5 bg-base-200 rounded-lg">
      <h2 class="card-title justify-between">
        <span>{{ module.name || '-' }}</span>
        <div
          :class="'btn btn-outline btn-sm btn-circle' + (isEditModuleName && ' hidden')"
          @click="isEditModuleName = !isEditModuleName"
        >
          <i class="fa-solid fa-pen cursor-pointer h-3 w-3" />
        </div>
      </h2>
      <input
        type="text"
        placeholder="Digite o nome do Módulo e pressione Enter"
        class="input input-bordered input-sm w-full"
        v-model="module.name"
        v-if="isEditModuleName"
        @keydown.enter="isEditModuleName = !isEditModuleName"
      />

      <div class="card-actions justify-end items-center">
        Selecionar para Download
        <input
          type="checkbox"
          class="checkbox checkbox-primary"
          v-model="module.selected"
          :indeterminate="
            module.selected && module.pages.some(lesson => !lesson.selected) ||
            !module.selected && module.pages.some(lesson => lesson.selected)"
        />
        <span @click="showContent = !showContent">
          <button
            v-if="showContent"
            class="btn btn-sm btn-error btn-outline"
          >
            <i class="fa-solid fa-eye-slash" />
          </button>
          <button
            v-else
            class="btn btn-sm btn-success"
          >
            <i class="fa-solid fa-eye" />
          </button>
        </span>
      </div>

      <div v-if="showContent" class="flex flex-col gap-3 max-h-96 h-full overflow-y-auto border-2 border-accent rounded-lg py-2 px-1">
        <div class="p-2 flex justify-center w-full">
          <input
            class="input input-bordered input-sm w-3/4"
            placeholder="Pesquisar conteúdo..."
            v-model="searchContent"
          />
        </div>
        <ModuleContent :module="module" :search="searchContent" />
      </div>
    </div>
  </div>
  `
}