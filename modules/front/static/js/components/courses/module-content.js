export default {
  props: {
    module: Object,
    search: String,
  },
  data() {
    return {
      lessons: this.module.pages,
    }
  },
  template: `
  <div class="card w-full" v-for="lesson in module.pages.filter(lesson => lesson.name.toLowerCase().includes(search.toLowerCase()))">
    <div class="card-body px-2 py-1 bg-base-300 w-full">
      <h2 class="card-title justify-between">
        <span>{{ lesson.name || '-' }}</span>
        <button
          :class="'btn btn-outline btn-sm btn-circle' + (lesson.isEditLessonName && ' hidden')"
          @click="lesson.isEditLessonName = !lesson.isEditLessonName"
        >
          <i class="fa-solid fa-pen cursor-pointer h-3 w-3" />
        </button>
      </h2>
      <input
        type="text"
        placeholder="Digite o nome da Aula e pressione Enter"
        class="input input-bordered input-sm w-full"
        v-model="lesson.name"
        v-if="lesson.isEditLessonName"
        @keydown.enter="lesson.isEditLessonName = !lesson.isEditLessonName"
      />

      <div class="card-actions justify-end items-center">
        Selecionar para Download
        <input type="checkbox" class="checkbox checkbox-primary" v-model="lesson.selected" />
      </div>
    </div>
  </div>
  `
}