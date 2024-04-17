-- Este arquivo SQL mantém os dados base da aplicação. A tabela Platform não deve ter as IDs alteradas.

INSERT OR IGNORE INTO Settings (key, value) VALUES
('last_executed_at', '0'),
('user_consent', '0'),
('download_path', 'Cursos/'),
('user_os', ''),
('use_original_media_name', '0')
('download_subtitles', '0')
('default_user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'),
('get_product_extra_info', '0'),
('download_widevine', '0'),
('widevine_cdm_path', ''),
('bento4_toolbox_path', 'SYSTEM'),
('scan_html_for_videos', '0'),
('use_custom_ffmpeg', '0'),
('custom_ffmpeg_path', 'SYSTEM'),
('download_threads', '2');


INSERT OR IGNORE INTO MediaDeliverySources (name, description) VALUES 
('Arquivo Direto (HTTP)', 'Arquivo hospedado pela plataforma'),
('Link Drive', 'Link de compartilhamento do Google Drive'),
('Video Nativo HLS', 'Video hospedado pela própria plataforma'),
('Youtube', 'Vídeo hospedado no Youtube'),
('Vimeo', 'Vídeo hospedado no Vimeo'),
('PandaVideo', 'Vídeo hospedado no PandaVideo. Pode conter dados ou usar o Widevine'),
('SafeVideo', 'Vídeo hospedado no SafeVideo. Existe um segmento de 6 segundos a cada ~24 segundos com dados na tela.'),
('API', 'Conteúdo acessado por meio de API'),
('HTML', 'Conteúdo acessado por meio de HTML');

INSERT OR IGNORE INTO DRMTypes (name, description) VALUES 
('VISUAL', 'DRM FALSO, onde a plataforma renderiza dados do lado do cliente, não existem dados nos arquivos baixados'),
('SOCIAL', 'DRM REAL, porém a proteção se dá por meio de impor "medo de responsabilidade" ao usuário, como marca dágua com nome do usuário, etc. Será baixado normalmente, usuários mal intencionados simplesmente usam dados falsos sempres, a lei pressupõe inocência, então desde que você não compartilhe os arquivos baixados, não há infração legal.'),
('REAL', 'DRM real, como Widevine, PlayReady, FairPlay, etc. Pode até ser baixado dependendo da boa vontade dos mantenedore$. Não é coisa que usuários leigos conseguiram fazer por precisar lidar com chaves e requisições. Download desativado por padrão'),
('ONLINE PASS', 'DRM que requer conexão com a internet para funcionar. Será baixado mas tal proteção não será removida em nenhum cenário.'),
('OFFLINE PASS', 'DRM do tipo arquivo com senha. Será baixado normalmente, mas a senha não será removida. O usuário terá que inserir a senha manualmente para acessar o conteúdo baixado.'),
('MIXED', 'Conteúdo com mais de um tipo de proteção, como por exemplo, conteúdo com DRM REAL e SOCIAL ao mesmo tempo.');

INSERT OR IGNORE INTO MediaTypes (name, description) VALUES 
('Video', 'Conteúdo de vídeo'),
('Audio', 'Conteúdo de áudio'),
('Texto', 'Conteúdo de texto'),
('Imagem', 'Conteúdo de imagem'),
('Apresentação', 'Conteúdo de apresentação (Powerpoint/slides)'),
('Planilha', 'Conteúdo de planilha (Excel, Sheets, csv)'),
('PDF', 'Conteúdo de PDF (livros, apostilas, etc.'),
('Documento', 'Conteúdo de documento(Docx, ODT, HTML, etc.)'),
('Aplicativo', 'Conteúdo de aplicativo (APK, EXE, etc.)'),
('Código', 'Conteúdo de código (Normalmente arquivos "src.zip", específico para cursos de programação)'),
('E-book', 'Conteúdo de e-book (PDF, EPUB, etc.)'),
('Outro', 'Conteúdo de outro tipo não previsto na lista (pfv abra issue se encontrar)');

-- Plataformas previstas a ter suporte em primeiro momento
INSERT OR IGNORE INTO Platforms (name, description, landing_page, content_delivery_type) VALUES 
('Hotmart', 'Conteúdo variado, desde cursos livres até e-books e software, de áreas diferentes', 'https://hotmart.com/', 'MIXED'),
('Udemy', 'Cursos livres de diversas áreas', 'https://udemy.com/', 'MIXED'),
('Kiwify', 'Conteúdo variado, desde cursos livres até e-books de diversas áreas', 'https://kiwify.com.br/', 'API'),
-- ('Astron Members', 'Conteúdo mais voltado para as áreas de Marketing, Design e Programação', 'https://www.astronmembers.com.br', 'MIXED'),
-- ('EBAC', 'Cursos livres de diversas áreas', 'https://ebaconline.com.br/', 'API'),
-- ('Alura', 'Cursos livres da área de TI', 'https://www.alura.com.br', 'MIXED'),
-- ('Unhide School', 'Cursos livres da área de Design e Ilustração', 'https://unhideschool.com/', 'API'),
-- ('Rocket Seat', 'Cursos livres da área de TI', 'https://www.rocketseat.com.br/', 'API'),
-- ('Treina Web', 'Cursos livres da área de TI', 'https://www.treinaweb.com.br', 'API'),
('School Of Net', 'Cursos livres da área de TI', 'https://www.schoolofnet.com/', 'API'),
('Full Cycle', 'Cursos de especialização em TI', 'https://fullcycle.com.br/', 'API');
-- ('Estratégia Medicina', 'Cursos preparatórios para a área de Medicina', 'https://med.estrategia.com', 'API'),
-- ('Estratégia Concursos', 'Cursos preparatórios para concursos públicos', 'https://www.estrategiaconcursos.com.br/', 'MIXED'),
-- ('Estratégia Jurídico', 'Cursos preparatórios para a área de Direito', 'https://cj.estrategia.com/', 'API'),
-- ('Alfacon', 'Cursos preparatórios para concursos públicos', 'https://www.alfaconcursos.com.br', 'API'),
-- ('SanarFlix', 'Cursos preparatórios para a área de Medicina', 'https://www.sanarflix.com.br/', 'API'),
-- ('Medway', 'Cursos preparatórios para a área de Medicina', 'https://medway.com.br/', 'API'),
-- ('Manole', 'Cursos preparatórios para a área de Medicina', 'https://www.manole.com.br', 'HTML'),
-- ('EEPHCFMUSP', 'Cursos preparatórios para a área de Medicina', 'https://eephcfmusp.org.br/portal/', 'HTML'),
-- ('Medcel', 'Cursos preparatórios para a área de Medicina', 'https://www.medcel.com.br/', 'API'),
-- ('MedCurso', 'Cursos preparatórios para a área de Medicina', 'https://www.medcurso.com.br/', 'API'),
-- ('MedCof', 'Cursos preparatórios para a área de Medicina', 'https://www.medcof.com.br/', 'HTML')


-- Associações de plataformas com tipos de DRM
-- INSERT INTO PlatformDRM (platform_id, drm_type_id) VALUES 
-- (1, 1), -- Associa 'Hotmart' com 'SOCIAL'
-- (1, 2); -- Associa 'Hotmart' com 'REAL'
-- Repetir para as demais plataformas conforme o aplicativo for elaborado