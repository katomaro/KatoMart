export default {
  template: `
  <div class="bg-gray-800 rounded-lg overflow-hidden shadow-lg text-white p-6">
    <div class="flex justify-center">
      <img class="rounded-full w-32 h-32 object-cover border-2 border-primary" src="https://avatars.githubusercontent.com/u/112831443?&v=4" alt="Foto do Github de Felipe (Yuu)">
    </div>
    <div class="text-center mt-4">
      <h2 class="font-bold text-xl mb-2 text-pink-500">Felipe Adeildo</h2>
      <h3 class="font-bold text-l mb-2 text-red-500">Desenvolvedor Front-End Fixo</h3>
      <p class="text-gray-400 text-sm">Responsabilidade no Projeto:</p>
      <p class="text-gray-200 text-sm italic">
        <span class="text-pink-500">Estudante de Front-End, responsável integral e autoridade máxima pela UI/UX do usuário.</span> Também atua corrigindo bugs pontuais e prestando suporte à comunidade por integrar à mesma.
      </p>
      <p class="text-gray-200 text-sm italic">
        Felipe é um estudante de programação e matemática, possui algumas
        <span class="tooltip" data-tip="certificados">
          <a href="https://drive.google.com/drive/folders/1Jl3jlpc-Je1mnatpO3k0-HnpMH_Zh_C_?usp=drive_link" class="text-pink-500 text-gray-200 text-sm italic hover:underline hover:text-pink-700" target="_blank" >
              medalhas
          </a>
        </span> em olimpíadas de matemática e computação.
        Atualmente trabalha com <span class="text-accent">Python</span> e <span class="text-accent">TypesScript</span> utilizando fremworks/bibliotecas como <span class="text-accent">ReactJs</span>, <span class="text-accent">NextJs</span>, <span class="text-accent">FastAPI</span>, <span class="text-accent">Flask</span>, etc.
      </p>
    </div>
    <div class="grid grid-cols-2 gap-2 mt-4">
      <a href="mailto:oie.eu.sou.um@gmail.com" class="btn btn-primary flex items-center justify-center gap-2">
        <i class="fas fa-envelope"></i> Email
      </a>
      <a href="https://linkedin.com/in/felipe-adeildo" class="btn btn-primary flex items-center justify-center gap-2">
        <i class="fas fa-globe"></i> Linkedin
      </a>
      <a href="https://github.com/felipe-adeildo" class="btn btn-primary flex items-center justify-center gap-2">
        <i class="fab fa-github"></i> Github
      </a>
      <a href="https://t.me/sr_yuu" class="btn btn-primary flex items-center justify-center gap-2">
        <i class="fab fa-telegram"></i> Telegram
      </a>
    </div>
    <div class="mt-4 text-sm font-bold">
      <p class="text-center">
        Formas de DOAÇÃO:
        <div role="alert" class="alert alert-warning font-normal text-xs py-1">
          <i class="fa-solid fa-triangle-exclamation"></i>
          <span>Não contabilizadas para o <a href="https://github.com/katomaro/katomart" class="text-pink-500 hover:underline hover:text-pink-700">Katomart</a> em hipótese alguma por não ser o responsável principal do projeto.</span>
        </div>
      </p>
      <div class="flex flex-wrap gap-2 justify-center my-2">
        <div class="badge badge-accent">
          <div class="tooltip" data-tip="Nubank">
            <div class="flex items-center gap-1">
              <i class="fa-brands fa-pix"></i> PIX: oie.eu.sou.um@gmail.com
            </div>
          </div>
        </div>
          <div class="badge badge-accent">
            <a href="https://picpay.me/sr_yuu" class="flex items-center gap-1">
              <i class="fa-solid fa-sack-dollar"></i> Picpay
            </a>
          </div>
          <div class="badge badge-accent">
            <div class="tooltip" data-tip="Banco do Brasil">
              <div class="flex items-center gap-1">
                <i class="fa-brands fa-pix"></i> PIX: felipe.adeildo0@gmail.com
              </div>
            </div>
          </div>
      </div>
    </div>
  </div>
  `
}