const { ref, toRefs } = Vue
import { DRM_STATUS_COLOR_LIST, DRM_STATUS_MESSAGE_LIST } from "../../constants.js"
import { sanitizeString } from "../../utils.js"
import CourseContentModal from "./course-content-modal.js"

export default {
  components: { CourseContentModal },
  props: {
    course: Object,
  },
  setup(props) {
    const { course } = toRefs(props)
    course.value.data.name = sanitizeString(course.value.data.name)
    const isModalOpen = ref(false)
    const isEditCourseName = ref(false)
    const tempCourseName = ref(course.value.data.name)

    const editCourseName = () => {
      if (tempCourseName.value) {
        course.value.data.name = sanitizeString(tempCourseName.value)
        isEditCourseName.value = false
      }
    }

    return {
      isModalOpen,
      isEditCourseName,
      tempCourseName,
      editCourseName,
      sanitizeString,
    }
  },
  computed: {
    drmColor() {
      return 'badge-' + DRM_STATUS_COLOR_LIST[this.course.data.drm_enabled]
    },
    drmMessage() {
      return DRM_STATUS_MESSAGE_LIST[this.course.data.drm_enabled]
    }
  },
  template: `
  <div class="card w-full max-w-xl bg-base-200 shadow-xl">
    <div class="card-body">
      <h2 class="card-title text-center justify-between">
        <span>{{ course.data.name }}</span>
        <button
          :class="'btn btn-outline btn-sm btn-circle' + (isEditCourseName && ' hidden')"
          @click="isEditCourseName = !isEditCourseName"
        >
          <i class="fa-solid fa-pen cursor-pointer h-3 w-3" />
        </button>
      </h2>
      <input
        type="text"
        placeholder="Digite o nome do Curso e pressione Enter"
        class="input input-bordered input-sm w-full"
        :value="tempCourseName"
        @input="tempCourseName = sanitizeString($event.target.value)"
        @keydown.enter="editCourseName"
        v-if="isEditCourseName"
      />

      <div class="flex justify-end items-center gap-2">
        <div
          :class="['badge', drmColor, 'mr-2']">
        {{ drmMessage }}
        </div>
        <div class="badge badge-secondary mr-2">
          {{ course.data.status }}
        </div>
      </div>

      <div class="card-actions justify-end items-center gap-2">
        Selecionar para Download
        <input type="checkbox" class="checkbox checkbox-primary" v-model="course.selected" />
        <button
          class="btn btn-primary btn-sm"
          @click="isModalOpen = !isModalOpen"
          :disabled="!course.selected || isModalOpen"
        >
          <i class="fa-solid fa-hand" />
          Selecionar Conteúdo
        </button>
      </div>
    </div>
  </div>

  <CourseContentModal
    :course="course"
    :isModalOpen="isModalOpen"
    @close-modal-request="isModalOpen = false"
    @set-course-modules="course.data.modules = $event"
  />
  `
}