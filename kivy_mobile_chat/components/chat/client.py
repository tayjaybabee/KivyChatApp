"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-20 12:36:21
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-21 20:50:33
FilePath: kivy_mobile_chat/components/chat/client.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
import socket
import threading
from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type
from kivy_mobile_chat.log_engine import ROOT_LOGGER as PARENT_LOGGER, Loggable
from kivy_mobile_chat.components.chat.server.helpers import process_requests, freeze_on_connect

MOD_LOGGER = PARENT_LOGGER.get_child('components.chat.client')

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6967


class ChatClient(Loggable):
    def __init__(
            self,
            update_ui_callback,
            host=DEFAULT_HOST,
            port=DEFAULT_PORT,
            username=None,
    ):
        super().__init__(MOD_LOGGER)
        log = self.class_logger
        self.__host = None
        self.__port = None
        self.__socket = None
        self.__username = None

        if username:
            self.username = username

        self.update_ui_callback = update_ui_callback
        self.host = host
        self.port = port

        self.socket = None
        self._stop_event = threading.Event()

    @property
    def config_frozen(self):
        """
        Returns whether the configuration is frozen. If the client is connected, the configuration is frozen. This is 
        because the configuration is frozen when this class's socket attribute is not None, or when the `connected` 
        property is True.
        
        Returns:
            bool:
                Whether the configuration is frozen.
        """
        return self.connected or self.socket is not None

    @property
    def connected(self) -> bool:
        return self.socket is not None and self.socket.fileno() != -1

    @property
    def host(self) -> str:
        """
        The host IP address of the server.
        
        Returns:
            str:
                The host IP address.
        """
        return self.__host

    @host.setter
    @validate_type(str)
    @freeze_on_connect
    def host(self, new):
        if self.config_frozen:
            raise AttributeError("Host cannot be changed.")

        self.__host = new

    @property
    def port(self) -> int:
        """
        The port number of the server.
        """
        return self.__port

    @port.setter
    @validate_type(int)
    @freeze_on_connect
    def port(self, new):
        if self.config_frozen:
            raise AttributeError("Port cannot be changed.")

        self.__port = new

    @property
    def socket(self) -> 'socket':
        """
        The socket object used to communicate with the server.
        """
        return self.__socket

    @socket.setter
    @freeze_on_connect
    def socket(self, new):
        if self.config_frozen:
            raise AttributeError("Socket cannot be changed.")

        self.__socket = new

    @property
    def username(self) -> str:
        """
        The username of the client.
        """
        return self.__username

    @username.setter
    @validate_type(str)
    def username(self, new):
        # TODO: Send new username to server
        self.__username = new

    def connect(self, username=None):
        """Attempts to connect to the server and starts receiving messages."""
        if username is None and self.__username is None:
            self.class_logger.error("Username required.")
            return
        elif username is not None:
            self.username = username

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.settimeout(10)  # Added timeout to avoid indefinite waiting in case of network issues
        try:
            self.socket.connect((self.__host, self.__port))

            self._stop_event.clear()
            self.receiver_thread = threading.Thread(target=self.receive_message)
            self.receiver_thread.start()
        except socket.error as e:
            self.class_logger.error(f"Failed to connect: {e}")

    def disconnect(self):
        """Closes the socket and marks the client as disconnected."""
        self._stop_event.set()
        if self.socket:
            self.socket.close()
        if hasattr(self, 'receiver_thread') and self.receiver_thread is not threading.current_thread():
            try:
                self.receiver_thread.join()  # Ensure the receiving thread shuts down gracefully
            except RuntimeError as e:
                self.class_logger.error(f"Error while joining receiver thread: {e}")

    def send_message(self, message):
        """Sends a message to the server."""
        if self.connected and self.socket:
            try:
                self.socket.sendall(message.encode('utf-8', 'ignore'))
            except socket.error as e:
                self.class_logger.error(f"Error sending message: {e}")

    def receive_message(self):
        """Receives messages from the server and updates the UI."""
        while self.connected and not self._stop_event.is_set():
            try:
                data = self.socket.recv(1024).decode()
                data = process_requests(data, self)
                if data:
                    self.update_ui_callback(data)
                else:
                    continue
            except socket.error as e:
                self.class_logger.error(f"Error receiving message: {e}")
                self.disconnect()
