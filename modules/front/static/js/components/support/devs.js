import KatomaroCard from './cards/katomaro.js'
import YuuCard from './cards/yuu.js'

export default {
  components: {
    KatomaroCard,
    YuuCard
  },
  setup() {
    const cards = [
      KatomaroCard,
      YuuCard
    ]

    return {
      cards
    }
  },
  template: `
  <section class="my-2">
    <h1 class="text-3xl font-bold text-center mb-8">
      <i class="fas fa-code"></i> Desenvolvedores responsáveis pelo projeto
    </h1>

    <div class="container max-w-6xl mx-auto bg-base-100 shadow-xl rounded-lg p-6 border-2 border-primary">
      <strong class="text-pink-500">AOS DESENVOLVEDORES PASSADOS:</strong> por favor 
      enviem uma PR para o repositório adicionando o seu card e descrevendo como você contribuiu
      para o projeto. Siga o modelo abaixo.

      <div class="grid grid-cols-3 gap-4 mt-4">
        <component v-for="(card, index) in cards" :key="index" :is="card" />
      </div>
  </div>
  </section>
  `
}