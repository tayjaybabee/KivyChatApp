"""
Author: Taylor B. tayjaybabee@gmail.com
Date: 2024-10-20 11:27:45
LastEditors: Taylor B. tayjaybabee@gmail.com
LastEditTime: 2024-10-20 19:36:03
FilePath: kivy_mobile_chat/components/ui/panels/user_connection.py
Description: 这是默认设置,可以在设置》工具》File Description中进行配置
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class UserConnectionPanel(BoxLayout):
    def __init__(self, connect_callback, **kwargs):
        super(UserConnectionPanel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.connect_callback = connect_callback
    
        self.username_input = TextInput(hint_text='Enter your username', size_hint=(1, 0.1))
        self.add_widget(self.username_input)
    
        self.connect_btn = Button(text='Connect', size_hint=(1, 0.1))
        # Correct the binding to use the proper method
        self.connect_btn.bind(on_press=self.on_connect_pressed)
        self.add_widget(self.connect_btn)


    def on_connect_pressed(self, instance):
        if self.username_input.text.strip():
            self.connect_callback(self.username_input.text)
