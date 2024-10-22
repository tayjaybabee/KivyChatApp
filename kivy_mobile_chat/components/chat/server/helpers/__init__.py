"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-21 18:43:45
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-21 20:52:51
FilePath: kivy_mobile_chat/components/chat/server/helpers/__init__.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
from kivy_mobile_chat.log_engine import ROOT_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('components.chat.server.helpers')


from kivy_mobile_chat.components.chat.server.helpers.decorators import freeze_on_connect


def request_lookup(request):
    log = MOD_LOGGER.get_child('request_lookup')
    request = request.strip().upper()
    log.debug(f'Looking up request: {request}')
    res = REQUEST_MAP.get(request, None)
    
    if res:
        log.debug(f'Request found: {request}')
        return res
    else:
        log.debug(f'Request not found: {request}')
        return None


def send_pong(client):
    log = MOD_LOGGER.get_child('send_pong')
    log.debug('Sending PONG')
    client.send_message('PONG')


def process_requests(data, client):
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    request = request_lookup(data)
    if request:
        request(client)
        client.class_logger.debug(f'Processed request: {data}')
    else:
        client.class_logger.debug(f'Unknown request: {data}')
        print(f'Unknown request: {data}')
        return data
    
    
def send_username(client):
    log = MOD_LOGGER.get_child('send_username')
    log.debug('Sending answer to username request')
    client.send_message(client.username)
        


REQUEST_MAP = {
    'PING': send_pong,
    'NICKNAME_REQUEST': send_username,
}
