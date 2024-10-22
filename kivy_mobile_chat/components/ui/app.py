"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-21 19:18:49
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-21 19:20:30
FilePath: kivy_mobile_chat/components/ui/app.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_mobile_chat.components.ui import UserConnectionPanel, ChatInterface
from kivy_mobile_chat.components.chat import ChatClient


class ChatApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.client = ChatClient(self.update_chat_interface, self.on_connection_success)
        self.login_panel = UserConnectionPanel(self.client.connect)
        self.chat_interface = ChatInterface(self.client.send_message)

        self.root.add_widget(self.login_panel)
        return self.login_panel

    def append_messge(self, message):
        if self.chat_interface and self.chat_interface.msg_label:
            self.chat_interface.msg_label.text += f'\n{message}'

    def on_connection_success(self):
        self.root.clear_widgets()
        self.root.add_widget(self.chat_interface)

    def update_chat_interface(self, message):
        from kivy.clock import Clock
        Clock.schedle_once(lambda dt: self.append_message(message))
