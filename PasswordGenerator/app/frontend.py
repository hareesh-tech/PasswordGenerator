import logging
import pyperclip

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from .backend import DatabaseManager, PasswordGenerator

logger = logging.getLogger(__name__)

KV = '''
#:import RoundedRectangle kivy.graphics.vertex_instructions.RoundedRectangle

<EnterpriseButton@Button>:
    background_normal: ''
    background_color: 0,0,0,0
    bold: True
    color: 1,1,1,1
    canvas.before:
        Color:
            rgba: 0.39, 0.40, 0.95, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [24,]
        Color:
            rgba: 0.55, 0.36, 0.98, 0.6
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [24,]

BoxLayout:
    orientation: 'vertical'
    padding: 40
    spacing: 30

    canvas.before:
        Color:
            rgba: 0.06, 0.09, 0.16, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "PassFort"
        font_size: "34sp"
        bold: True
        color: 0.39, 0.40, 0.95, 1
        size_hint_y: 0.1

    # Length Card
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.28
        padding: 25
        spacing: 15

        canvas.before:
            Color:
                rgba: 0.12, 0.16, 0.25, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [20,]

        Label:
            text: "Password Length"
            color: 0.8, 0.85, 0.95, 1
            bold: True
            size_hint_y: 0.3

        BoxLayout:
            spacing: 20

            Slider:
                id: length_slider
                min: 8
                max: 64
                value: 16
                step: 1
                on_value: app.on_slider_change(self.value)

            TextInput:
                id: length_input
                text: "16"
                multiline: False
                size_hint_x: 0.1
                width: 50
                size_hint_y: 0.3
                length: 40
                font_size: "16sp"
                padding: [10,10]
                halign: "center"
                background_color: 0.18, 0.22, 0.33, 1
                foreground_color: 1,1,1,1
                cursor_color: 0.55, 0.36, 0.98, 1
                input_filter: "int"
                on_text_validate: app.on_input_change(self.text)

    Widget:
        size_hint_y: 0.1

    EnterpriseButton:
        text: "GENERATE PASSWORD"
        size_hint_y: 0.15
        font_size: "18sp"
        on_press: app.generate_password()
'''

class PassFortApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = DatabaseManager()
        self.generator = PasswordGenerator()
        self.current_password = None

    def build(self):
        Window.size = (500, 650)
        self.title = "PassFort"
        return Builder.load_string(KV)

    def on_slider_change(self, value):
        self.root.ids.length_input.text = str(int(value))

    def on_input_change(self, text):
        if text:
            value = int(text)
            if 8 <= value <= 64:
                self.root.ids.length_slider.value = value

    def generate_password(self):
        length = int(self.root.ids.length_slider.value)

        password = self.generator.generate(length=length)

        if password:
            self.current_password = password
            self.show_password_popup(password)

    # -------------------------------
    #  PASSWORD POPUP
    # -------------------------------

    def show_password_popup(self, password):

        content = BoxLayout(orientation='vertical', spacing=25, padding=30)

        content.add_widget(Label(
            text="Generated Password",
            font_size='16sp',
            color=(0.7,0.75,0.9,1)
        ))

        content.add_widget(Label(
            text=password,
            font_size='24sp',
            bold=True,
            color=(1,1,1,1)
        ))

        btn_box = BoxLayout(spacing=20)

        copy_btn = self.create_enterprise_button("Copy")
        copy_btn.bind(on_press=lambda x: self.copy_to_clipboard(password))

        save_btn = self.create_enterprise_button("Save")
        save_btn.bind(on_press=lambda x: self.show_save_dialog(password))

        btn_box.add_widget(copy_btn)
        btn_box.add_widget(save_btn)

        content.add_widget(btn_box)

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.85, 0.45),
            background='',
            background_color=(0.12, 0.16, 0.25, 1)
        )

        popup.open()

    # -------------------------------
    # SAVE WITH UID POPUP
    # -------------------------------

    def show_save_dialog(self, password):

        layout = BoxLayout(orientation='vertical', spacing=20, padding=30)

        layout.add_widget(Label(
            text="Enter Unique ID (UID)",
            color=(0.8,0.85,0.95,1)
        ))

        uid_input = TextInput(
            multiline=False,
            font_size='16sp',
            padding=[10,10],
            background_color=(0.18, 0.22, 0.33, 1),
            foreground_color=(1,1,1,1),
            size_hint_y=0.6
        )

        layout.add_widget(uid_input)

        btn_box = BoxLayout(spacing=20)

        save_btn = self.create_enterprise_button("Save")
        cancel_btn = self.create_enterprise_button("Cancel")

        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)

        layout.add_widget(btn_box)

        popup = Popup(
            title="",
            content=layout,
            size_hint=(0.75, 0.4),
            background='',
            background_color=(0.12, 0.16, 0.25, 1)
        )

        def save_action(instance):
            uid = uid_input.text.strip()
            if uid:
                if self.db_manager.save_password(uid, password):
                    popup.dismiss()
                    self.show_message("Saved successfully")
            else:
                self.show_message("UID required")

        save_btn.bind(on_press=save_action)
        cancel_btn.bind(on_press=popup.dismiss)

        popup.open()

    # -------------------------------

    def create_enterprise_button(self, text):
        return Button(
            text=text,
            background_normal='',
            background_color=(0.39, 0.40, 0.95, 1),
            color=(1,1,1,1),
            bold=True
        )

    def copy_to_clipboard(self, password):
        pyperclip.copy(password)
        self.show_message("Copied to clipboard")

    def show_message(self, message):
        popup = Popup(
            title='',
            content=Label(text=message, color=(1,1,1,1)),
            size_hint=(0.5, 0.25),
            background='',
            background_color=(0.12, 0.16, 0.25, 1)
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)