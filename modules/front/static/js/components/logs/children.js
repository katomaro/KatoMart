import ChildItem from "./child-item.js";


export default {
  name: 'CourseChildren',
  props: {
    children: Array,
  },
  components: {
    ChildItem
  },
  data() {
    return {
      isOpen: false,
      query: ""
    }
  },
  methods: {
    filterChildren() {
      return this.query ?
        this.children.filter(child => child.name.toLowerCase().includes(this.query.toLowerCase())) :
        this.children;
    },
    getChildren(child) {
      return child.modules || child.lessons || child.files || null
    }
  },
  computed: {
    filteredChildren() {
      return this.children.filter(child => child.name.toLowerCase().includes(this.query.toLowerCase()))
    }
  },
  template: `
    <div class="bg-base-200 rounded-lg p-2">
      <h2 class="flex justify-center items-center gap-2">
        <input
          v-model="query"
          class="input input-sm w-full"
          placeholder="Pesquisar Conteúdo"
          @keyup="isOpen = true"
        />
        <div class="tooltip tooltip-left" :data-tip="isOpen ? 'Clique para fechar' : 'Clique para expandir'">
          <button
            :class="['btn', isOpen ? 'btn-error' : 'btn-success', 'btn-sm btn-circle']"
            @click="isOpen = !isOpen"
            v-if="children.length > 0"
          >
          {{ isOpen ? '🔼' : '🔽' }}
          </button>
        </div>
      </h2>

      <div v-if="isOpen" class="mt-2 flex flex-col gap-1 max-h-[65vh] h-full overflow-y-auto">
        <div v-for="child in filteredChildren" :key="child.id" class="border-2 border-base-300 rounded-lg p-1">
          <ChildItem :child="child" />
          <CourseChildren
            v-if="getChildren(child) && getChildren(child).length > 0"
            :children="getChildren(child)"
          />
        </div>
        <div
          v-if="filteredChildren.length === 0"
          class="text-center alert alert-info">
            Nenhum Conteúdo encontrado
        </div>
      </div>
    </div>
  `
}
