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