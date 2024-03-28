const { ref, toRefs } = Vue

export default {
  props: {
    course: Object,
  },
  setup(props) {
    const { course } = toRefs(props)
    const isModalOpen = ref(false)
    const isEditCourseName = ref(false)
    const tempCourseName = ref(course.value.subdomain)

    const editCourseName = () => {
      if (tempCourseName.value) {
        course.value.subdomain = tempCourseName.value
        isEditCourseName.value = false
      }
    }

    return {
      isModalOpen,
      isEditCourseName,
      tempCourseName,
      editCourseName,
    }
  },
  template: `
  <div class="card w-full max-w-xl bg-base-200 shadow-xl">
    <div class="card-body">
      <h2 class="card-title text-center justify-between">
        <span>{{ course.subdomain }}</span>
        <div>
          <div class="badge badge-secondary mr-2">{{ course.status }}</div>
          <button :class="'btn btn-outline btn-sm btn-circle' + (isEditCourseName && ' hidden')" @click="isEditCourseName = !isEditCourseName">
            <i class="fa-solid fa-pen cursor-pointer h-3 w-3" />
          </button>
        </div>
      </h2>
      <input
        type="text"
        placeholder="Digite o nome do Curso e pressione Enter"
        class="input input-bordered input-sm w-full"
        v-model="tempCourseName"
        v-if="isEditCourseName"
        @keydown.enter="editCourseName"
      />
      <div class="card-actions justify-end items-center gap-2">
        Selecionar par Download
        <input type="checkbox" class="checkbox checkbox-primary" v-model="course.selected" />
        <button class="btn btn-primary btn-sm" @click="isModalOpen = !isModalOpen" :disabled="!course.selected || isModalOpen">Selecionar Conteúdo</button>
      </div>
    </div>
  </div>

  <input type="checkbox" class="modal-toggle" v-model="isModalOpen" />
  <div className="modal" role="dialog">
    <div className="modal-box w-full max-w-7xl">
      <h3 class="font-bold text-lg">Conteúdo do Curso {{ course.subdomain }}</h3>

      <p>Conteúdo do curso será carregado aqui bla bla bla</p>

      <div className="modal-action justify-end">
        <button class="btn" @click="isModalOpen = !isModalOpen">Fechar</button>
      </div>
    </div>
  </div>
  `
}