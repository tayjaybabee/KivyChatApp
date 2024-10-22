"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-22 07:51:59
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-22 08:39:03
FilePath: kivy_mobile_chat/config/servers.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
from dataclasses import dataclass
from dataclasses import field
import pickle
from platformdirs import PlatformDirs
from pathlib import Path


CONFIG_FILE_NAME = 'config.ini'
PLATFORM_DIRS = PlatformDirs('TestGUI', 'Inspyre-Softworks')
DEFAULT_CONFIG_DIR = Path(PLATFORM_DIRS.user_config_dir).resolve()
DEFAULT_CONFIG_FILE_PATH = DEFAULT_CONFIG_DIR.joinpath(CONFIG_FILE_NAME)
DEFAULT_SERVER_FILE_DIR = DEFAULT_CONFIG_DIR.joinpath('servers')


@dataclass
class Server:
    
    name: str = field(
        default='',
        metadata={
            'description': 'The name of the server.',
            'type': 'str',
            'required': True
        }
    )
    
    host: str = field(
        default='localhost', 
        metadata={
            'description': 'The host address of the server.', 
            'type': 'str',
            'required': True
        }
    )
    
    port: int = field(
        default=6967, 
        metadata={
            'description': 'The port number of the server.', 
            'type': 'int',
            'required': True
        }
    )
    
    username: str = field(
        default='', 
        metadata={
            'description': 'The username of the client.', 
            'type': 'str',
            'required': True
        }
    )
    
    def __post_init__(self):
        if not self.name:
            raise ValueError('Server name is required.')
        
        if not self.host:
            raise ValueError('Server host is required.')
        
        if not self.username:
            raise ValueError('Username is required.')
        
        
    @property
    def config_file_path(self) -> Path:
        return DEFAULT_SERVER_FILE_DIR.joinpath(f'{self.name}.pkl')
        
    def save(self, file_path: Path = None):
        if not self.config_file_path.parent.exists():
            self.config_file_path.parent.mkdir(parents=True)
            
        with open(self.config_file_path, 'wb') as file:
            pickle.dump(self.__dict__, file)

    @classmethod
    def load(cls, file_path: Path):
        with open(file_path, 'rb') as file:
            return Server(**pickle.load(file))
        
        
def get_server_files(server_dir: Path = DEFAULT_SERVER_FILE_DIR):
    """
    Get all server files in the given directory.
    
    Parameters:
        server_dir (Path):
            The directory to search for server files.
            
    Returns:
        List[Path]:
            A list of all server files in the given directory.
    """
    return server_dir.glob('*.pkl')


def get_server_names(server_dir: Path = DEFAULT_SERVER_FILE_DIR):
    """
    Get the names of all servers in the given directory.
    
    Parameters:
         server_dir (Path):
                The directory to search for server files.
                
    Returns:
        List[str]:
            A list of all server names in the given directory.
    """
    return [file.stem for file in get_server_files(server_dir)]


def load_all_servers(server_dir: Path = DEFAULT_SERVER_FILE_DIR):
    """
    Load all servers in the given directory.
    
    Parameters:
        server_dir (Path):
            The directory to search for server files.
            
    Yields:
        Server:
            A generator that yields all servers in the given directory.
            
    Raises:
        Exception:
            If an error occurs while loading a server file.
    """
    for file in get_server_files(server_dir):
        try:
            yield Server.load(file)
        except Exception as e:
            print(f'Error loading server file {file}: {e}')
