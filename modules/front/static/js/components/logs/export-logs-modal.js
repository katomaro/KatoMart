export default {
  props: {
    query: Object
  },
  data() {
    return { isOpen: false, includeSensitiveData: false }
  },

  methods: {
    toggleModal() {
      this.isOpen = !this.isOpen
    },
  },

  template: `
  <div class="tooltip tooltip-info tooltip-left absolute right-4" data-tip="Exportar Logs">
    <button class="btn btn-accent" @click="toggleModal()">
      <i class="fa-solid fa-file-export"></i>
    </button>
  </div>


  <input type="checkbox" class="modal-toggle" v-model="isOpen" />
  <div class="modal" role="dialog">
    <div class="modal-box">
      <button
        class="modal-close btn btn-sm btn-circle fixed right-2 top-2"
        @click="toggleModal()">
          x
      </button>
      <h3
        class="font-bold text-lg flex items-center justify-center">
          Exportar Logs <i class="fa-solid ml-2 fa-file-export" />
      </h3>

      <form action="/api/export_logs" method="post" class="flex flex-col gap-4 items-center">
        <div class="form-control w-full">
          <label class="label">
            <span class="label-text">Incluir Dados Sensíveis?</span>
          </label>
          <input type="checkbox" class="checkbox checkbox-primary" name="include_sensitive_data" v-model="includeSensitiveData" />
        </div>

        <div class="form-control w-full" v-if="includeSensitiveData">
          <label class="label">
            <span class="label-text">Dados sensíveis serão substituídos por</span>
          </label>
          <input type="text" value="*" class="input input-bordered w-full" name="sensitive_data_replacement" disabled />
        </div>

        <button class="btn btn-primary" @click="toggleModal()">
          Exportar
        </button>
      </form>
    </div>
  </div>
  `
}