export default {
  props: {
    query: Object
  },
  data() {
    return { isOpen: false }
  },

  methods: {
    toggleModal() {
      this.isOpen = !this.isOpen
    }
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

      <p>Vai aparecer um formulário aqui em algum momento, nos próximos commits, vrau!</p>
    </div>
  </div>
  `
}