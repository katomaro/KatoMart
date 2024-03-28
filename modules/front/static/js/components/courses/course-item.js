export default {
  props: {
    course: Object,
  },
  template: `
  <div class="card w-full max-w-xl bg-base-200 shadow-xl">
    <div class="card-body">
      <h2 class="card-title text-center">{{ course.subdomain }}</h2>
      <div class="card-actions justify-end items-center gap-2">
        Selecionar par Download
        <input type="checkbox" class="checkbox checkbox-primary" />
        <button class="btn btn-primary btn-sm">Selecionar Conteúdo</button>
      </div>
    </div>
  </div>
  `
}