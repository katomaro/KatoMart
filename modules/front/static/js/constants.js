export const GITHUB_MASTER_URL = 'https://raw.githubusercontent.com/katomaro/katomart/master';
export const GITHUB_VERSION_URL = `${GITHUB_MASTER_URL}/VERSIONS.json`;
export const GITHUB_NOTICE_URL = `${GITHUB_MASTER_URL}/AVISO.html`;

export const CONTRIBUTIONS_URL = "https://raw.githubusercontent.com/katomaro/katomart/master/CONTRIBUTIONS.json";
export const EXPENSES_URL = "https://raw.githubusercontent.com/katomaro/katomart/master/EXPENSES.json";


export const DOWNLOAD_STATUS_COLOR_MAP = {
  Baixando: "warning",
  Completo: "success",
  Erro: "error",
  "Não Iniciado": "info"
}

// Placeholders Examples
export const COURSES_PLACEHOLDER_EXAMPLE = [
  {
    id: 1,
    name: "Como Desenhar Hentai - Kato 3.0",
    status: "Baixando",
    progress: 0.7,
    children: [
      {
        id: '1.1',
        name: "Módulo 1 - Ahegao",
        status: "Completo",
        progress: 1,
        children: []
      },
      {
        id: '1.2',
        name: "Módulo 2 - Shota",
        status: "Completo",
        progress: 1,
        children: []
      },
      {
        id: '1.3',
        name: "Módulo 3 - Milf",
        status: "Baixando",
        progress: 0.5,
        children: [
          {
            id: '1.3.1',
            name: "Aula 1",
            status: "Completo",
            progress: 1,
            downloadedThings: ['Video', 'PDF', 'Audio', 'Texto'],
          },
          {
            id: '1.3.1',
            name: "Aula 2",
            status: "Completo",
            progress: 1,
            downloadedThings: ['Video', 'PDF', 'Audio', 'Texto'],
          },
          {
            id: '1.3.1',
            name: "Aula 3",
            status: "Baixando",
            progress: 0,
            downloadedThings: [],
          },

          {
            id: '1.3.1',
            name: "Aula 3",
            status: "Não Iniciado",
            progress: 0,
            downloadedThings: [],
          }
        ]
      },
      {
        id: '1.4',
        name: "Módulo 4 - Posições",
        status: "Não Iniciado",
        progress: 0,
        children: []
      }
    ]
  },
  {
    id: 2,
    name: "Outro curso só de exemplo",
    status: "Não Iniciado",
    progress: 0,
    children: []
  }
]

export const LOGS_PLACEHOLDER_EXAMPLE = {
  total: 10,
  logs: [
    { id: 1, message: "O bot morreu, eeeee", level: "error", date: "2022-10-20 10:00:00", sensitive: true },
    { id: 2, message: "O bot começou a funcionar novamente!", level: "info", date: "2022-10-20 10:00:01", sensitive: false },
    { id: 3, message: "Erro ao baixar um arquivo, vai tentar de novo", level: "warn", date: "2022-10-20 10:00:02", sensitive: true },
    { id: 4, message: "Aula baixada com sucesso!", level: "info", date: "2022-10-20 10:00:03", sensitive: false },
    { id: 5, message: "Iniciando download de vídeo", level: "debug", date: "2022-10-20 10:00:04", sensitive: true },
    { id: 6, message: "Esperando 5 segundos antes de tentar novamente...", level: "info", date: "2022-10-20 10:00:05", sensitive: false },
    { id: 7, message: "Course concluído", level: "info", date: "2022-10-20 10:00:06", sensitive: false },
    { id: 8, message: "Erro fatal ao baixar um pdf", level: "error", date: "2022-10-20 10:00:07", sensitive: true },
    { id: 9, message: "Iniciando download de audio", level: "debug", date: "2022-10-20 10:00:08", sensitive: true },
    { id: 10, message: "Iniciando download de video", level: "debug", date: "2022-10-20 10:00:09", sensitive: true },
  ]
}