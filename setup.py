import general_utils as general_utils
from setup_texts import SETUP_TEXTS

CLONE_DIRECTORY = general_utils.get_execution_path()

USER_LANGUAGE = None
USER_OS = None
USER_LOCAL_PASSWORD = None

HAS_FFMPEG = None
INSTALL_FFMPEG = None

HAS_GECKODRIVER = None
INSTALL_GECKODRIVER = None

HAS_BENTO4 = None
INSTALL_BENTO4 = None

SUPPORTED_PYTHON_VERSION = (3, 12)
SUPPORTED_OS = ('win32', 'linux', 'darwin')

# Multi-language support will be implemented at a later date as the project grows.
#
# for language in SETUP_TEXTS:
#     print(SETUP_TEXTS[language]['which_language'])
# USER_LANGUAGE = input()
# 
# if USER_LANGUAGE not in setup_utils.SUPPORTED_LANGUAGES.values():
#     print('Unsupported language. Defaulting to English.')
#     USER_LANGUAGE = 'en'

USER_LANGUAGE = 'pt'

print(SETUP_TEXTS[USER_LANGUAGE]['welcome'])

print(SETUP_TEXTS[USER_LANGUAGE]['check_python_version'])
if not general_utils.check_python_support(*SUPPORTED_PYTHON_VERSION):
    raise Exception(SETUP_TEXTS[USER_LANGUAGE]['python_version_not_supported'])
print(SETUP_TEXTS[USER_LANGUAGE]['python_version_supported'])

print(SETUP_TEXTS[USER_LANGUAGE]['check_user_os'])
USER_OS = general_utils.get_operating_system()
if USER_OS not in SUPPORTED_OS:
    raise Exception(SETUP_TEXTS[USER_LANGUAGE]['unsupported_os'])
print(SETUP_TEXTS[USER_LANGUAGE]['supported_os'])

# MASTER PASSWORD
# Descomentar quando a funcionalidade for implementada
# USER_LOCAL_PASSWORD = input(SETUP_TEXTS[USER_LANGUAGE]['prompt_master_password'])

# CLI TOOLS
print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_introduction'])

# FFMPEG
print(SETUP_TEXTS[USER_LANGUAGE]['ffmpeg_introduction'])
print(SETUP_TEXTS[USER_LANGUAGE]['check_for_cli_tool'].format('ffmpeg'))
HAS_FFMPEG = general_utils.check_for_cli_tool('ffmpeg')
if not HAS_FFMPEG:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_not_located'].format('ffmpeg'))
else:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_located'].format('ffmpeg'))
    INSTALL_FFMPEG = False
while True and not HAS_FFMPEG:
    try:
        INSTALL_FFMPEG = general_utils.get_user_third_party_optin(tool_name='ffmpeg')
        break
    except ValueError:
        print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_optin_input_error'])
        continue
if not INSTALL_FFMPEG:
    print(SETUP_TEXTS[USER_LANGUAGE]['ffmpeg_download_instructions'])

# GECKODRIVER
print(SETUP_TEXTS[USER_LANGUAGE]['geckodriver_introduction'])
print(SETUP_TEXTS[USER_LANGUAGE]['check_for_cli_tool'].format('geckodriver'))
HAS_GECKODRIVER = general_utils.check_for_cli_tool('geckodriver')
if not HAS_GECKODRIVER:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_not_located'].format('geckodriver'))
else:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_located'].format('geckodriver'))
    INSTALL_GECKODRIVER = False
while True and not HAS_GECKODRIVER:
    try:
        INSTALL_GECKODRIVER = general_utils.get_user_third_party_optin(tool_name='geckodriver')
        break
    except ValueError:
        print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_optin_input_error'])
        continue
if not INSTALL_GECKODRIVER:
    print(SETUP_TEXTS[USER_LANGUAGE]['geckodriver_download_instructions'])

# MP4DECRYPT
print(SETUP_TEXTS[USER_LANGUAGE]['bento4_introduction'])
print(SETUP_TEXTS[USER_LANGUAGE]['check_for_cli_tool'].format('bento4'))
HAS_BENTO4 = general_utils.check_for_cli_tool('mp4decrypt')
if not HAS_BENTO4:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_not_located'].format('bento4'))
else:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_located'].format('bento4'))
    INSTALL_BENTO4 = False
while True and not HAS_BENTO4:
    try:
        INSTALL_BENTO4 = general_utils.get_user_third_party_optin(tool_name='bento4')
        break
    except ValueError:
        print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_optin_input_error'])
        continue
if not INSTALL_BENTO4:
    print(SETUP_TEXTS[USER_LANGUAGE]['bento4_download_instructions'])


# INSTALLATION
general_utils.clear_screen(user_os=USER_OS)
general_utils.create_venv(venv_path='.')
general_utils.install_requirements(venv_path='.', requirements_path='requirements.txt')
general_utils.create_startup_script(user_platform=USER_OS,
                                  venv_path=CLONE_DIRECTORY,
                                  start_string=SETUP_TEXTS[USER_LANGUAGE]['start_string'],
                                  batch_name=SETUP_TEXTS[USER_LANGUAGE]['batch_name'])

CONFIGS = {
    'setup_user_language': USER_LANGUAGE,
    'setup_user_os': USER_OS,
    'setup_has_ffmpeg': HAS_FFMPEG,
    'setup_install_ffmpeg': INSTALL_FFMPEG,
    'setup_has_geckodriver': HAS_GECKODRIVER,
    'setup_install_geckodriver': INSTALL_GECKODRIVER,
    'setup_has_bento4': HAS_BENTO4,
    'setup_install_bento4': INSTALL_BENTO4
}

general_utils.write_config_file(config=CONFIGS)

print(SETUP_TEXTS[USER_LANGUAGE]['setup_complete'].format(SETUP_TEXTS[USER_LANGUAGE]['batch_name'], 'bat' if USER_OS == 'win32' else 'sh'))
