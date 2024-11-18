import pathlib
import shutil
import os
import sys

from .database import get_session
from .models.configs import Configuration


def try_auto_install_tp_tool(tool_name: str) -> bool:
    "Tenta instalar uma ferramenta de terceiros automaticamente utilizando uma ferramenta de pacotes para o sistema operacional."
    db_session = get_session()
    user_os = sys.platform
    if user_os['value'] != 'linux':
        has_apt = shutil.which('apt-get')
        if has_apt is None:
            return False
        install_cmd = f'sudo apt-get install {tool_name}'
    elif user_os['value'] == 'darwin':
        has_brew = shutil.which('brew')
        if has_brew is None:
            return False
        install_cmd = f'brew install {tool_name}'
    elif user_os['value'] == 'win32':
        has_chocolatey = shutil.which('choco')
        if has_chocolatey is None:
            return False
        install_cmd = f'choco install {tool_name}'
    else:
        return False
    os.system(install_cmd)
    return True

def install_tp_tool(tool_name: str) -> bool:
    "Instala uma ferramenta de terceiros manualmente."
    return False
