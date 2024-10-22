"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-21 20:17:15
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-21 20:17:55
FilePath: kivy_mobile_chat/components/chat/server/helpers/decorators.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
from functools import wraps


def freeze_on_connect(func):
    """
    Decorator that prevents modification of a property after the client has established a connection.
  
    Raises:
        AttributeError:
            If manipulation of the decorated property is attempted after a connection has been established.
    """

    @wraps(func)
    def wrapper(self, value):
        if self.config_frozen:
            raise AttributeError(f'{func.__name__} cannot be changed once a connection is established!')
        return func(self, value)

    return wrapper
