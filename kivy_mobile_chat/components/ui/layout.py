"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-19 18:24:46
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-21 18:51:27
FilePath: kivy_mobile_chat/components/ui/layout.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
# *******************************************
#  Copyright (c) 2024. Inspyre Softworks    *
# *******************************************
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import socket
import threading
from kivy_mobile_chat.log_engine import ROOT_LOGGER, Loggable
from kivy_mobile_chat.components.ui.panels.user_connection import UserConnectionPanel


MOD_LOGGER = ROOT_LOGGER.get_child('components.ui.app')


class ChatInterface(BoxLayout):
    def __init__(self, send_callback, **kwargs):
        super().__init__(**kwargs)
        self.__class_logger = MOD_LOGGER.get_child('ChatInterface')
        self.orientation = 'vertical'
        self.send_callback = send_callback
        
        self.msg_label = Label(size_hint=(1, 0.9))
        self.add_widget(self.msg_label)
        
        self.input_box = TextInput(size_hint=(1, 0.1), multiline=False)
        self.add_widget(self.input_box)
        
        self.send_btn = Button(text='Send', size_hint=(1, 0.1))
        self.send_btn.bind(on_press=self.on_send_pressed)
        self.add_widget(self.send_btn)
        
        self.class_logger.debug('ChatInterface created')
        
    @property
    def class_logger(self):
        return self.__class_logger
    
    def create_child_logger(self, child_name):
        return self.class_logger.get_child(child_name)

    def on_send_pressed(self, instance):
        text = self.input_box.text.strip()
        if text:
            self.send_callback(text)
            self.input_box.text = ''

# class ChatLayout(BoxLayout):
#     def __init__(self, **kwargs):
#         """
#         ChatLayout class to handle the layout of the chat app
#         
#         Parameters:
#             **kwargs:
#                 The keyword arguments passed to the class.
#                 
#         Returns:
#             None
# 
#         Raises:
#             None
#         """
#         self.class_logger = MOD_LOGGER.get_child('ChatLayout')
#         super().__init__(**kwargs)
#         
#         self.orientation = 'vertical'
#         self.padding = 10
#         
#         self.connection_panel = UserConnectionPanel()
#         self.connection_panel.bind(on_connection_success=self.setup_chat_interface)
#         self.add_widget(self.connection_panel)
# 
#         # User input for username
#         self.username_input = TextInput(hint_text='Enter your username', size_hint=(1, 0.1))
#         self.add_widget(self.username_input)
#         
#         self.connect_btn = Button(text='Connect', size_hint=(1, 0.1))
#         self.connect_btn.bind(on_press=self.connect_to_server)
#         self.add_widget(self.connect_btn)
# 
#         # Area to display chat messages
#         self.msg_label = Label(size_hint=(1, 0.8))
#         self.add_widget(self.msg_label)
# 
#         # User input for messages
#         self.input_box = TextInput(size_hint=(1, 0.1), multiline=False)
#         self.add_widget(self.input_box)
# 
#         # Send button
#         self.send_btn = Button(text='Send', size_hint=(1, 0.1))
#         self.send_btn.bind(on_press=self.send_message)
#         self.add_widget(self.send_btn)
# 
#         self.socket = None
# 
#     def connect_to_server(self, instance):
#         """
#         Connect to the server
#         
#         Parameters:
#             instance:
#                 The instance of the button that was pressed. 
# 
#         Returns:
#             None
#         """
#         if self.username_input.text.strip() and not self.socket:
#             self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.host = 'localhost'
#             self.port = 6967
#             try:
#                 self.socket.connect((self.host, self.port))
#                 threading.Thread(target=self.receive_message, daemon=True).start()
#             except Exception as e:
#                 self.msg_label.text = f'Connection failed: {str(e)}'
# 
# 
#     def send_message(self, instance):
#         """
#         Send a message to the server.
#         
#         Parameters:
#             instance:
#                 The instance of the button that was pressed.
# 
#         Returns:
#             None
# 
#         """
#         log = self.class_logger.get_child('send_message')
#         log.debug('Sending message')
#         if self.username_input.text.strip() and self.input_box.text.strip():
#             log.debug(f'Message from {self.username_input.text}: {self.input_box.text}')
#             message = f"{self.username_input.text}: {self.input_box.text}"
#             self.socket.sendall(message.encode())
#             self.input_box.text = ''
# 
#     def setup_chat_interface(self, instance, *args):
#         self.remove_widget(self.connection_panel)
#         
#         self.msg_label = Label(size_hint=(1, 0.0))
#         self.add_widget(self.msg_label)
# 
#     def receive_message(self):
#         """
#         Receive messages from the server.
# 
#         Returns:
#             None
#         """
#         while True:
#             try:
#                 data = self.socket.recv(1024).decode()
#                 if data == 'NICKNAME_REQUEST':
#                     self.socket.sendall(self.username_input.text.encode())
#                 elif data == 'PING':
#                     self.socket.sendall('PONG'.encode())
#                 elif data:
#                     self.msg_label.text += f"\n{data}"
#                 else:
#                     break  # Server has likely closed the connection
#             except Exception as e:
#                 self.msg_label.text = f'Error: {str(e)}'
#                 break
# 
#     def on_stop(self):
#         """
#         Close the socket when the app is stopped.
#             
#         Returns:
#             None
#         """
#         if self.socket:
#             self.socket.close()
