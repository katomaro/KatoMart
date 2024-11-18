import json
import os
import pathlib
import shutil
import subprocess
import sys
import re


SUPPORTED_LANGUAGES = {
    'portugues': 'pt',
    'english': 'en'
}


def sanitize_path_component(component):
    # Trim leading/trailing spaces
    component = component.strip()
    
    # Split into base and extension (in case of filenames)
    base, ext = os.path.splitext(component)
    
    # Define invalid characters for file/directory names across Windows, Linux, MacOS
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
    
    # Remove invalid characters from base and extension
    invalid_chars_re = re.compile(invalid_chars)
    base = invalid_chars_re.sub('', base)
    ext = invalid_chars_re.sub('', ext)
    
    # Remove leading/trailing periods and spaces from base
    base = base.strip(' .')
    
    # Ensure the base name is not empty
    if not base:
        base = 'file_k' if ext else 'folder_k'  # Default to 'file_k' for filenames and 'folder_k' for others
    
    # Reserved names in Windows (case-insensitive)
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        *(f'COM{i}' for i in range(1, 10)),
        *(f'LPT{i}' for i in range(1, 10))
    }
    
    # Append '_k' if the base name is a reserved name
    if base.upper() in reserved_names:
        base += '_k'
    
    # Reconstruct the sanitized component
    sanitized_component = base + ext
    
    return sanitized_component


def remaining_path_length(path: pathlib.Path, os_type: str) -> int:
    max_lengths = {
        'win32': 260,
        'darwin': 1024,
        'linux': 4096
    }
    max_length = max_lengths.get(os_type, 260)

    current_length = len(str(path.resolve()))
    
    remaining = max_length - current_length
    return remaining

def get_execution_path() -> str:
    """Get the path of the current script
    Returns:
        str: The path of the current script
    """
    return os.path.dirname(os.path.abspath(__file__))

def clear_screen(user_os: str='win32') -> None:
    """Clear the screen
    Params:
        tool_name (str): The name of the tool
    """
    if user_os == 'win32':
        os.system('cls')
    elif user_os in ('linux', 'darwin'):
        os.system('clear')

def check_python_support(major: int=3, minor: int=12) -> bool:
    """Check if the Python version is supported
    Params:
        major (int): The major version of Python
        minor (int): The minor version of Python
    """
    return sys.version_info.major == major and sys.version_info.minor >= minor

def check_for_cli_tool(tool_name: str=''):
    """Check if a CLI tool is installed
    Params:
        tool_name (str): The name of the tool
    """
    return shutil.which(tool_name) is not None

def get_operating_system() -> str:
    """Get the operating system name
    Returns:
        str: The operating system name
    """
    operating_system = sys.platform
    return operating_system if operating_system in ['linux', 'win32', 'darwin'] else 'unsupported'

def get_user_third_party_optin(tool_name: str='') -> tuple[bool, bool]:
    """Get the user's choice for installing a third party tool
    Params:
        tool_name (str): The name of the tool
    Returns:
        bool: Whether the user wants to install the tool
    """
    user_input = input(f'{tool_name.capitalize()} (download, skip): ')
    if user_input.lower() == 'download':
        return True
    elif user_input.lower() == 'skip':
        return False
    else:
        raise ValueError

def create_venv(venv_path: str='.') -> None:
    """Create a virtual environment in the specified path."""
    subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)

def install_requirements(venv_path: str='.', requirements_path: str='requirements.txt'):
    """Install packages using pip from a requirements file in the created virtual environment."""
    pip_executable = os.path.join(venv_path, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'pip')
    subprocess.run([pip_executable, 'install', '-r', requirements_path], check=True)

def create_startup_script(user_platform: str='win32', venv_path: str='.', start_string: str='', batch_name: str='') -> None:
    if user_platform == 'win32':
        create_windows_batch(venv_path=venv_path, start_string=start_string, batch_name=batch_name)
    elif user_platform in ['linux', 'darwin']:
        create_unix_script(venv_path=venv_path, start_string=start_string, batch_name=batch_name)

def create_windows_batch(venv_path: str='.', start_string: str='', batch_name: str='') -> None:
    batch_path = os.path.join(venv_path, batch_name + '.bat')
    batch_content = f"""
@echo off
echo {start_string}
call "{os.path.join(venv_path, 'Scripts', 'activate')}"
set "PYTHONPATH=%PYTHONPATH%;{os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))}"
set "FLASK_APP={os.path.join(venv_path, 'servidor', 'app.py')}"
set "FLASK_ENV=production"
"{os.path.join(venv_path, 'Scripts', 'flask')}" run --port=6102
pause
"""
    with open(batch_path, 'w') as file:
        file.write(batch_content)

def create_unix_script(venv_path: str='.', start_string: str='', batch_name: str=''):
    batch_path = os.path.join(venv_path, batch_name + '.sh')
    script_content = f"""
#!/bin/bash
echo "{start_string}"
source "{os.path.join(venv_path, 'bin', 'activate')}"
export PYTHONPATH="$PYTHONPATH:{os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))}"
export FLASK_APP="{os.path.join(venv_path, 'servidor', 'app.py')}"
export FLASK_ENV=development
"{os.path.join(venv_path, 'bin', 'flask')}" run --port=6102
"""
    with open(batch_path, 'w') as file:
        file.write(script_content)
    os.chmod(batch_path, 0o755)

def write_config_file(config: dict, config_path: str='config.json') -> None:
    """Write the configuration file
    Params:
        config (dict): The configuration dictionary
        config_path (str): The path to the configuration file
    """
    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

def read_and_delete_config_file(config_path: str='config.json') -> dict:
    """Read the configuration file and returns its contents as well as deleting the file
    Params:
        config_path (str): The path to the configuration file
    Returns:
        dict: The configuration parameters
    """
    # TODO set default to all false
    if not os.path.exists(config_path):
        return None
    configs = {}
    with open(config_path, 'r') as file:
        configs = json.load(file)
    os.remove(config_path)
    return configs
