SETUP_TEXTS = {
    'pt': {
        'unsupported_os': 'Desculpe, seu sistema operacional não é suportado por este aplicativo.\nSaindo.',
        'which_language': '[pt] Digite o idioma que deseja utilizar (para continuar em português, digite: pt):',
        'welcome': 'Boas vindas ao utilitário de instalação do Katomart!\n\n'
                    + 'Este utilitário irá verificar se você possui as ferramentas de sistema necessárias para '
                    'executar o Katomart\n\t' + 'Caso você não possua alguma das ferramentas, '
                    'o utilitário irá te explicar sua necessidade e te perguntar se você deseja tentar uma instalacao '
                    'automática, ou, te guiar em como instalar cada uma manualmente.\n\n'
                    + 'Nem todas as ferramentas são necessárias, mas, melhoram a experiência!'
                    + ' (Este utilitário não instala as ferramentas, apenas verifica a presença delas, e o uso do programa em si deve seguir a jurisdição aplicável no país)',
        'check_python_version': 'Verificando sua versão do Python (versão mínima: 3.12)...',
        'python_version_not_supported': '\tDesculpe, sua versão do Python não é suportada por este aplicativo.\nAtualize-a (este script não interfere com o Python do usuário por risco de quebrar aplicações terceiras).',
        'python_version_supported': '\tSua versão do Python é suportada por este aplicativo!',
        'check_user_os': 'Verificando seu sistema operacional...',
        'unsupported_os': '\tDesculpe, seu sistema operacional não é suportado por este aplicativo.\nSaindo.',
        'supported_os': '\tSeu sistema operacional é suportado por este aplicativo!',
        'prompt_master_password': 'Digite a senha mestra a ser utilizada para acessar sua instância do Katomart:\n',
        'cli_tool_introduction': 'Agora, vamos verificar se você possui as ferramentas de sistema instaladas e explicar uma por uma.\n',
        'check_for_cli_tool': '\tVerificando se a ferramenta "{}" está instalada...',
        'cli_tool_not_located': '\tA ferramenta "{}" não foi localizada.\n' +
                                '\t\tDigite "download" para indicar que o programa deverá tentar realizar o download da ferramenta.\n' +
                                '\t\tDigite "skip" para ignorar a instalação desta ferramenta.\n',
        'cli_tool_located': '\tA ferramenta "{}" foi localizada em seu sistema com sucesso!',
        'ffmpeg_introduction': 'O FFMPEG é uma ferramenta que permite a manipulação de arquivos de áudio e vídeo. '
                                'Ele é necessário para a execução de algumas funcionalidades do Katomart que lidam com a codificação e normalização de vídeos.\n',
        'ffmpeg_download_instructions': 'Para instalar o FFMPEG, siga as instruções abaixo:\n' +
                                        '1. Acesse o site oficial do FFMPEG: https://ffmpeg.org/download.html\n' +
                                        '2. Baixe a versão mais recente do FFMPEG para o seu sistema operacional, de um distribuidor oficial (painel localizado à esquerda na página).\n' +
                                        '3. Extraia os arquivos e adicione o arquivo /bin/ffmpeg à variável "PATH" de suas Variáveis de Ambiente no seu sistema operacional.\n',
        'cli_tool_optin_input_error': 'Você deve digitar "download" ou "skip" apenas!',
        'geckodriver_introduction': 'O Geckodriver é uma ferramenta que permite a automação de navegadores web, e é necessário para alguns downloaders específicos funcionarem. Você também precisa ter o Firefox instalado.\n'
                                    + '\t#Boycott Manifest V3 (chromium)',
        'geckodriver_download_instructions': 'Para instalar o Geckodriver, siga as instruções abaixo:\n' +
                                            '1. Instale o Mozilla Firefox (caso não tenha instalado): https://www.mozilla.org/pt-BR/firefox/new/\n' +
                                            '2. Acesse a aba de releases do Github do Geckodriver e baixe a versão correspondente ao seu sistema: https://github.com/mozilla/geckodriver/releases\n' +
                                            '3. Extraia os arquivos e adicione o arquivo "geckodriver" à variável "PATH" de suas Variáveis de Ambiente no seu sistema operacional.\n',
        'bento4_introduction': 'O MP4Decrypt é uma ferramenta que faz parte do Bento4 que permite a descriptografia de arquivos de vídeo no formato MP4.\n' +
                                   'Ela é necessária apenas para baixar vídeos do Widevine, e para fazer esse processo você precisa de uma CDM válida de um ANDROID extraída pelo Frida.\n' +
                                   'Caso você não saiba o que é isso, pule a instalação desta ferramenta, pois isto não será ensinado aqui, e você pode sempre baixar mais tarde.\n',
        'bento4_download_instructions': 'Para instalar o MP4Decrypt, você precisa baixar o pacote do Bento4, para isto, siga as instruções abaixo:\n' +
                                             '1. Acesse o site oficial do Bento4: https://www.bento4.com/downloads/\n' +
                                             '2. Baixe a versão mais recente do Bento4 para o seu sistema operacional.\n' +
                                             '3. Extraia os arquivos e adicione o arquivo /bin/mp4decrypt à variável "PATH" de suas Variáveis de Ambiente no seu sistema operacional.\n',
        'start_string': 'Iniciando o Katomart...',
        'batch_name': 'executar_katomart',
        'setup_complete': 'Configuração concluída com sucesso! O Katomart está pronto para ser executado.\n '
                                                'Para iniciar o Katomart, execute o arquivo "{}.{}" que foi criado nesta pasta. Bons downloads :)'
    },
    'en': {
        'unsupported_os': 'Sorry, your operating system is not supported by this software.\nExiting.',
        'which_language': '[en] Type in the language you want to use (to continue in english, type: en):',
        'welcome': "Welcome to Katomart's setup script!\n\n"
                    + "This tool will make sure that you've got all the needed third party tools installed in your "
                    "system to run this Software\n\t" + 'If you are missing some, you will receive '
                    'an explanation as to why it is needed and will be given the option to attempt an auto-installation, or '
                    'be guided on how to download it yourself.\n\n'
                    + 'Not all tools are required to run this software, but they are highly recommended!'
                    + ' (This script does not install the tools, only checks for their presence, and the use of the software itself should follow the applicable jurisdiction in the country)',
        'check_python_version': 'Checking your Python version (minimum version: 3.12),,,',
        'python_version_not_supported': '\tSorry, your Python version is not supported by this software.\nPlease update it (this script does not interfere with the user\'s Python to avoid breaking third party applications).',
        'python_version_supported': '\tYour Python version is supported by this software!',
        'check_user_os': 'Checking your operating system...',
        'unsupported_os': '\tSorry, your operating system is not supported by this software.\nExiting.',
        'supported_os': '\tYour operating system is supported by this software!',
        'prompt_master_password': 'Type the master password to be used to access your Katomart instance:\n',
        'cli_tool_introduction': 'Now, we will be checking if you\'ve got the necessary third party system tools, as well as explain the need for each\n',
        'check_for_cli_tool': '\tchecking if the tool "{}" is installed...',
        'cli_tool_not_located': '\tThe tool "{}" was not found on your system.\n' +
                        '\t\tType "download" to flag this tool as desirable and for the software to attempt installing it in your system.\n' +
                        '\t\tType "skip" to ignore this tool completely.\n',
        'cli_tool_located': '\tThe tool "{}" was successfully located in your system!',
        'ffmpeg_introduction': 'FFMPEG is a tool that allows for the manipulation of audio and video files. '
                                'It is required for some of Katomart\'s functionalities that deal with video encoding and normalization.\n',
        'ffmpeg_download_instructions': 'To install FFMPEG, follow the instructions below:\n' +
                                        '1. Access the official FFMPEG website: https://ffmpeg.org/download.html\n' +
                                        '2. Download the latest version of FFMPEG for your operating system, from an official distributor (located on the left panel of the page).\n' +
                                        '3. Extract the files and add /bin/ffmpeg file to your system\'s "PATH" variable in your Environment Variables.\n',
        'cli_tool_optin_input_error': 'You must type only "download", or "skip"!',
        'geckodriver_introduction': 'Geckodriver is a tool that allows for web browser automation, and is required for some specific downloaders to work. You also need to have Firefox installed.\n'
                                    + '\t#Boycott Manifest V3 (chromium)',
        'geckodriver_download_instructions': 'To install Geckodriver, follow the instructions below:\n' +
                                            '1. Install Mozilla Firefox (if you haven\'t already): https://www.mozilla.org/en-US/firefox/new/\n' +
                                            '2. Access the releases tab on the Geckodriver Github page and download the version corresponding to your system: https://github.com/mozilla/geckodriver/releases\n' +
                                            '3. Extract the files and add the "geckodriver" file to your system\'s "PATH" variable in your Environment Variables.\n',
        'bento4_introduction': 'MP4Decrypt is a tool that is part of Bento4 that allows for the decryption of MP4 video files.\n' +
                                   'It is only required for downloading Widevine videos, and to do so you need a valid ANDROID CDM extracted through Frida.\n' +
                                   'If you don\'t know what this is, you SHOULD skip this, as it won\'t be taught here, and you can always download it later.\n',
        'bento4_download_instructions': 'To install MP4Decrypt, you need to download the Bento4 package, follow the instructions below:\n' +
                                             '1. Access the official Bento4 website: https://www.bento4.com/downloads/\n' +
                                             '2. Download the latest version of Bento4 for your operating system.\n' +
                                             '3. Extract the files and add /bin/mp4decrypt file to your system\'s "PATH" variable in your Environment Variables.\n',
        'start_string': 'Initializing Katomart...',
        'batch_name': 'run_katomart',
        'setup_complete': 'Setup completed successfully! Katomart is ready to be run.\n '
                                                'To start Katomart, run the "{}.{}" file that was created in this folder. Happy downloading :)'
    }
}