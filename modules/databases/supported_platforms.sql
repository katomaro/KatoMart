-- Este arquivo SQL mantém os dados base da aplicação. A tabela Platform não deve ter as IDs alteradas.

INSERT INTO DRMTypes (name, description) VALUES 
('VISUAL', 'DRM FALSO, onde a plataforma renderiza dados do lado do cliente, não existem dados nos arquivos baixados'),
('SOCIAL', 'DRM REAL, porém a proteção se dá por meio de impor "medo de responsabilidade" ao usuário, como marca dágua com nome do usuário, etc. Será baixado normalmente, usuários mal intencionados simplesmente usam dados falsos sempres, a lei pressupõe inocência, então desde que você não compartilhe os arquivos baixados, não há infração legal.'),
('REAL', 'DRM real, como Widevine, PlayReady, FairPlay, etc. Pode até ser baixado dependendo da boa vontade dos mantenedore$. Não é coisa que usuários leigos conseguiram fazer por precisar lidar com chaves e requisições. Download desativado por padrão'),
('ONLINE PASS', 'DRM que requer conexão com a internet para funcionar. Será baixado mas tal proteção não será removida em nenhum cenário.'),
('OFFLINE PASS', 'DRM do tipo arquivo com senha. Será baixado e por conveniência, na maioria dos casos a senha será removida automaticamente.')
('MIXED', 'Conteúdo com mais de um tipo de proteção, como por exemplo, conteúdo com DRM REAL e SOCIAL ao mesmo tempo.'),
('NONE', 'Conteúdo sem proteção alguma.');


-- Associações de plataformas com tipos de DRM
-- INSERT INTO PlatformDRM (platform_id, drm_type_id) VALUES 
-- (1, 1), -- Associa 'Hotmart' com 'SOCIAL'
-- (1, 2); -- Associa 'Hotmart' com 'REAL'
-- Repetir para as demais plataformas conforme o aplicativo for elaborado


-- Plataformas previstas a ter suporte em primeiro momento
INSERT OR REPLACE INTO Platforms(name, description, landing_page, content_delivery_type,) VALUES 
('Hotmart', 'Conteúdo variado, desde cursos livres até e-books e software, de áreas diferentes', 'https://hotmart.com/', 'MIXED'),
('Udemy', 'Cursos livres de diversas áreas', 'https://udemy.com/', 'MIXED'),
('Kiwify', 'Conteúdo variado, desde cursos livres até e-books de diversas áreas', 'https://kiwify.com.br/', 'API'),
('Astron Members', 'Conteúdo mais voltado para as áreas de Marketing, Design e Programação', 'https://www.astronmembers.com.br', 'MIXED'),
('EBAC', 'Cursos livres de diversas áreas', 'https://ebaconline.com.br/', 'API'),
('Alura', 'Cursos livres da área de TI', 'https://www.alura.com.br', 'MIXED'),
('Unhide School', 'Cursos livres da área de Design e Ilustração', 'https://unhideschool.com/', 'API'),
('Rocket Seat', 'Cursos livres da área de TI', 'https://www.rocketseat.com.br/', 'API'),
('Treina Web', 'Cursos livres da área de TI', 'https://www.treinaweb.com.br', 'API'),
('School Of Net', 'Cursos livres da área de TI', 'https://www.schoolofnet.com/', 'API'),
('Full Cycle', 'Cursos de especialização em TI', 'https://fullcycle.com.br/', 'API'),
('Estratégia Medicina', 'Cursos preparatórios para a área de Medicina', 'https://med.estrategia.com', 'API'),
('Estratégia Concursos', 'Cursos preparatórios para concursos públicos', 'https://www.estrategiaconcursos.com.br/', 'MIXED'),
('Estratégia Jurídico', 'Cursos preparatórios para a área de Direito', 'https://cj.estrategia.com/', 'API')
('Alfacon', 'Cursos preparatórios para concursos públicos', 'https://www.alfaconcursos.com.br', 'API'),
('SanarFlix', 'Cursos preparatórios para a área de Medicina', 'https://www.sanarflix.com.br/', 'API'),
('Medway', 'Cursos preparatórios para a área de Medicina', 'https://medway.com.br/', 'API'),
('Manole', 'Cursos preparatórios para a área de Medicina', 'https://www.manole.com.br', 'HTML'),
('EEPHCFMUSP', 'Cursos preparatórios para a área de Medicina', 'https://eephcfmusp.org.br/portal/', 'HTML'),
('Medcel', 'Cursos preparatórios para a área de Medicina', 'https://www.medcel.com.br/', 'API'),
('MedCurso', 'Cursos preparatórios para a área de Medicina', 'https://www.medcurso.com.br/', 'API'),
('MedCof', 'Cursos preparatórios para a área de Medicina', 'https://www.medcof.com.br/', 'HTML');
