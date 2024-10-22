"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-21 23:08:34
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-22 07:13:29
FilePath: test_gui.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
from pathlib import Path
import PySimpleGUI as psg
from platformdirs import PlatformDirs
from configparser import ConfigParser
from inspyre_toolbox.path_man import provision_path


CONFIG_FILE_NAME = 'config.json'
PLATFORM_DIRS = PlatformDirs('TestGUI', 'Inspyre-Softworks')
DEFAULT_CONFIG_DIR = Path(PLATFORM_DIRS.user_config_dir).resolve()
DEFAULT_CONFIG_FILE_PATH = DEFAULT_CONFIG_DIR.joinpath(CONFIG_FILE_NAME)

print(DEFAULT_CONFIG_FILE_PATH)


psg.theme('DarkAmber')


def create_config_file(config_file_path: Path = None):
    
    if config_file_path is None:
        config_file_path = DEFAULT_CONFIG_FILE_PATH
    else:
        config_file_path = provision_path(config_file_path)
        
    if not config_file_path.parent.exists():
        config_file_path.parent.mkdir()
    
    config = ConfigParser()
    config['DEFAULT'] = {
        'host': 'localhost',
        'port': '6967',
        'username': '',
    }
    with open(DEFAULT_CONFIG_FILE_PATH, 'w') as config_file:
        config.write(config_file)


def username_popup():
    return psg.popup_get_text('Enter your username:')


if __name__ == '__main__':
    username = username_popup()
    print(username)
    create_config_file()
