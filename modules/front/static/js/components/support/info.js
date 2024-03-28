export default {
  template: `
  <section>
    <h1 class="text-3xl font-bold text-center mb-8">
      <i class="fas fa-ticket-simple"></i> Suporte
    </h1>

    <div class="container max-w-6xl mx-auto bg-base-100 shadow-xl rounded-lg p-6 border-2 border-primary">
      <p>
        Se você está tendo problemas com o programa, antes de mais nada é
        <strong class="text-red-500">PRIMORDIAL</strong> que você verifique a aba de
        <a href="https://github.com/katomaro/katomart/issues" class="text-primary underline hover:text-primary-dark">
          SOLICITAÇÕES NO GITHUB!
        </a>
        NÃO ABRA PROBLEMAS <strong class="text-red-500">DUPLICADOS!</strong>
      </p>
      <p>
        Caso você não tenha encontrado um problema já existente, pedimos que você o
        registre naquela aba (isto requer uma conta do Github, que é grátis).
        Também pedimos que você forneça o máximo de detalhes possíveis, e se possível
        <a id="logbtn" href="{{ url_for('log') }}" class="text-primary underline hover:text-primary-dark">
          <i class="fas fa-layer-group"></i>
          Inclua LOGs gerados a partir do programa.
        </a>
        <strong class="text-red-500">
          CASO o log gerado CONTENHA dados SENSÍVEIS, envie-o por e-mail para
          <span class="text-pink-500">github@katomaro.com</span> EXCLUSIVAMENTE!
          e na descrição do problema, mencione que enviou o log por e-mail junto do
          assunto que contém o arquivo de log.
        </strong>
        Este e-mail é acessível apenas pelo desenvolvedor principal do programa
        <a href="https://www.github.com/katomaro" class="text-pink-500">@Katomaro</a>.
        Os logs serão armazenados até a resolução do problema e após isso, serão excluídos
        do servidor de e-mail e arquivos locais do desenvolvedor (não serão compartilhados
        com terceiros). Porém, você pode optar por deletar o log antes disso enviando um email para
        <span class="text-pink-500">dsar@katomaro.com</span> com o tema
        <span class="text-pink-500">"DELETAR LOG"</span> e no corpo do e-mail você
        de incluir:
        <ol class="my-1">
          <li>-> Seu nome completo</li>
          <li>-> Seu CPF</li>
          <li>-> Nome do arquivo anexado no e-mail original</li>
          <li>-> Motivo pelo qual deseja deletar o log</li>
        </ol>

        Da mesma forma, você pode solicitar o seu próprio log também por este e-mail,
        utilizando o assunto <span class="text-pink-500">"SOLICITAR LOG"</span>,
        o corpo do e-mail DEVE conter os itens citados anteriormente.
        As solicitações serão atendidas em até <strong class="text-red-500">
        7 dias úteis</strong>, e um e-mail de confirmação será enviado para você.
      </p>
      <p>
        Caso você não consiga acessar o Github, você pode pedir suporte
        <strong class="text-red-500">COMUNITÁRIO</strong> no grupo do Telegram:
        <a href="https://t.me/gatosdodois" class="text-pink-500 underline hover:text-pink-400">
            <strong>https://t.me/gatosdodois</strong>
        </a>.
        <strong class="text-red-500">NÃO ENVIE INFORMAÇÕES SENSÍVEIS NESTE GRUPO!</strong>
        Além disso, atente-se as regras do grupo que ficam nas mensagens fixadas,
        denotadas como <strong class="text-red-500">"Constituição Gatarial"</strong>.
        Lembre-se: Ao participar do grupo para falar sobre o programa, você continua sujeito
        aos termos que você concordou nos
        <a href="{{ url_for('agreement') }}" class="text-primary underline hover:text-primary-dark">
          Termos de Uso
        </a>.
      </p>
      <p>
        Por fim, lembre-se que ninguém é obrigado a te ajudar, o programa é de código livre,
        Se os colaboradores foram capazes de executar todo o trabalho, você também pode
        se esforçar um pouco, ou você pode contratar um desenvolvedor para te ajudar.
        <strong class="text-red-500">EXTREMAMENTE IMPORTANTE</strong> que você se atente
        à licença do programa, que está disponível no link
        <a href="https://github.com/katomaro/katomart/blob/master/LICENSE" class="text-pink-500 underline hover:text-pink-400">
          <strong>LICENÇA</strong>
        </a>. Enquanto a licença é bem permissiva,
        <strong class="text-red-500">TODA E QUALQUER ALTERAÇÃO deve referenciar o
        repositório original</strong> utilizar a mesma licença, o que implica que ele DEVE ser
        e ser disponibilizada publicamente além de ser de código aberto e creditando o repositório
        base.
      </p>
      <p>
        Além disso, é claro que todo o <strong class="text-pink-500">desenvolvimento
        tem um custo</strong>, tanto para procedimentos legais (que foram muitos para este
        projeto e ainda estão correndo) quanto para obtenção de acessos legais, a próxima
        seção é dedicada à creditar quem financiou o projeto. Agradeça-os principalmente,
        além dos desenvolvedores por suas INÚMERAS horas de vida gastas, ameaças judiciais
        enfrantadas, além de takendowns/dmcas, etc. Este repositório NÃO é brincadeira.
      </p>
      <div class="divider"></div>
      <p>Se o seu pedido de ajuda for para implementar uma plataforma ou um player,
        peço que entenda que existe toda uma burocracia legal necessária que você precisará fazer.
        Casp cpmtrário, a solicitação ficará lá em aberto. Você pode ajudar a obter o acesso
        contribuindo, porém, é sua responsabilidade em localizar um acesso barato. NADA de rateios,
        o acesso será obtido no meu nome, desde que caiba dentro do caixa do Katomart.
        <strong class="text-red-500">Também fique atento à solicitações já existentes
        quem contribuiu com acesso e/ou monetariamente tem prioridade nas requisições de suporte,
        e/ou implementações.
        </strong>
        </p>
        <div class="divider"></div>
        <p>
          <strong class="text-red-500">OS DESENVOLVEDORES RESERVAM-SE NO DIREITO DE TOMAR AÇÃO
          LEGAL CONTRA QUEM INFRINGIR A LICENÇA DO PROGRAMA! Se você é da turma que publica este
          projeto no 99Freelas e similares, saiba que você está infringindo a licença do programa,
          e nós somos notificados sempre que o repositório de código é transitado por estas plataformas
          de maneira automática. Grupos terceiros disponibilizando o Software sem a devida credibilidade
          também estão sujeitos a ação legal, segundo a licença mencionada. Se o grupo infringir direitos
          autorais, o grupo será notificado e o grupo terá 7 dias úteis para retirar o código do ar,
          e ao mesmo tempo os desenvolvedores formalizaram denúncia aos detentores de copyright da infração,
          e/ou provedores de serviço (serviços de hospedagem, sites, etc). Se o grupo não retirar o código
          do ar, os desenvolvedores tomarão ações legais contra o grupo, e o grupo será responsável por
          todos os custos legais e danos morais e materiais que a ação legal causar aos desenvolvedores.
          </strong>
          <div class="alert alert-warning text-lg flex justify-center my-1" role="alert">
            NÃO COMPACTUAMOS COM PIRATARIA, É CRIME!
          </div>
        </p>
        <div class="divider"></div>
      </div>
    </section>
`
}