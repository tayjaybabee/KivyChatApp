"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-21 21:08:15
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-21 21:28:08
FilePath: kivy_mobile_chat/components/chat/message.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """
    An enum to represent the direction of a message.
    """
    INCOMING = 'incoming'
    OUTGOING = 'outgoing'
    
    
class ComType(Enum):
    """
    An enum to represent the type of a message.
    """
    MESSAGE      = 'message'
    NOTIFICATION = 'notification'
    REQUEST      = 'request'
    RESPONSE     = 'response'
    
    

@dataclass
class Communique:
    """
    A class to represent a message object.
    """
    sender: str
    content: str
    timestamp: str
    direction: Direction
