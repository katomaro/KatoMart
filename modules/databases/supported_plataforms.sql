-- Este arquivo SQL mantém a relação básica de plataformas atualmente suportadas pelo sistema.

-- Plataformas previstas a ter suporte em primeiro momento
INSERT INTO Platforms(name, description, landing_page, content_delivery_type, has_drm, drm_type) VALUES 
('Hotmart', 'Conteúdo variado, desde cursos livres até e-books e software, de áreas diferentes', 'https://hotmart.com/', 'MIXED', 1, 'SOCIAL,REAL')
,('Udemy', 'Cursos livres de diversas áreas', 'https://udemy.com/', 'MIXED', 1, 'REAL')
,('Kiwify', 'Conteúdo variado, desde cursos livres até e-books de diversas áreas', 'https://kiwify.com.br/', 'API', 0, '')
,('Astron Members', 'Conteúdo mais voltado para as áreas de Marketing, Design e Programação', 'https://www.astronmembers.com.br', 'MIXED', 1, 'REAL')
,('EBAC', 'Cursos livres de diversas áreas', 'https://ebaconline.com.br/', 'API', 0, '')
,('Alura', 'Cursos livres da área de TI', 'https://www.alura.com.br', 'MIXED', 0, '')
,('Unhide School', 'Cursos livres da área de Design e Ilustração', 'https://unhideschool.com/', 'API', 1, 'REAL,SOCIAL,MONITOR')
,('Rocket Seat', 'Cursos livres da área de TI', 'https://www.rocketseat.com.br/', 'API', 1, 'MONITOR')
,('Treina Web', 'Cursos livres da área de TI', 'https://www.treinaweb.com.br', 'API', 1, 'MONITOR')
,('School Of Net', 'Cursos livres da área de TI', 'https://www.schoolofnet.com/', 'API', 1, 'MONITOR')
,('Full Cycle', 'Cursos de especialização em TI', 'https://fullcycle.com.br/', 'API', 1, 'REAL,MONITOR')
,('Estratégia Medicina', 'Cursos preparatórios para a área de Medicina', 'https://med.estrategia.com', 'API', 1, 'SOCIAL',)
,('Estratégia Concursos', 'Cursos preparatórios para concursos públicos', 'https://www.estrategiaconcursos.com.br/', 'MIXED', 1, 'SOCIAL,REAL')
,('Estratégia Jurídico', 'Cursos preparatórios para a área de Direito', 'https://cj.estrategia.com/', 'API', 1, 'SOCIAL')
,('Alfacon', 'Cursos preparatórios para concursos públicos', 'https://www.alfaconcursos.com.br', 'API', 1, 'SOCIAL')
,('SanarFlix', 'Cursos preparatórios para a área de Medicina', 'https://www.sanarflix.com.br/', 'API', 0, '')
,('Medway', 'Cursos preparatórios para a área de Medicina', 'https://medway.com.br/', 'API', 0, '')
,('Manole', 'Cursos preparatórios para a área de Medicina', 'https://www.manole.com.br', 'HTML', 0, '')
,('EEPHCFMUSP', 'Cursos preparatórios para a área de Medicina', 'https://eephcfmusp.org.br/portal/', 'HTML', 0, '')
,('Medcel', 'Cursos preparatórios para a área de Medicina', 'https://www.medcel.com.br/', 'API', 1, 'SOCIAL,MONITOR')
,('MedCurso', 'Cursos preparatórios para a área de Medicina', 'https://www.medcurso.com.br/', 'API', 1, 'REAL,SOCIAL,MONITOR')
,('MedCof', 'Cursos preparatórios para a área de Medicina', 'https://www.medcof.com.br/', 'HTML', 1, 'SOCIAL,MONITOR');