from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
import requests

# Foydalanuvchilar (login:parol)
USERS = {
    "Mirzo": "1234",
    "Maftuna": "5678"
}

# Firebase Realtime Database URL (REST API)
DB_URL = "https://mychatapp-d4fe1-default-rtdb.europe-west1.firebasedatabase.app/messages.json"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()
        bg = Image(source="background.jpg", allow_stretch=True, keep_ratio=False)
        root.add_widget(bg)

        title = Label(
            text="Salom",
            font_size=40,
            bold=True,
            color=(1,1,1,1),
            size_hint=(1,None),
            height=dp(80),
            pos_hint={"top":1}
        )
        root.add_widget(title)

        from kivy.uix.anchorlayout import AnchorLayout
        layout = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=(0,150,0,0))
        grid = GridLayout(cols=1, spacing=20, size_hint=(0.8,0.5))

        self.username = TextInput(hint_text="Login", multiline=False, size_hint=(1,None), height=dp(30), font_size=24)
        self.password = TextInput(hint_text="Parol", password=True, password_mask="*", multiline=False, size_hint=(1,None), height=dp(30), font_size=24)
        btn = Button(text="Kirish", size_hint=(1,None), height=dp(30), font_size=24,
                     background_color=(0.2,0.6,1,1), color=(1,1,1,1))
        btn.bind(on_press=self.do_login)

        grid.add_widget(self.username)
        grid.add_widget(self.password)
        grid.add_widget(btn)
        layout.add_widget(grid)
        root.add_widget(layout)
        self.add_widget(root)

    def do_login(self, instance):
        u,p = self.username.text, self.password.text
        if u in USERS and USERS[u]==p:
            self.manager.current = "chat"
            self.manager.get_screen("chat").set_user(u)

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

        root = FloatLayout()
        bg = Image(source="chat_bg.jpg", allow_stretch=True, keep_ratio=False, size_hint=(1,1))
        root.add_widget(bg)

        self.chat_area = GridLayout(cols=1, size_hint=(1,None), spacing=10, padding=10)
        self.chat_area.bind(minimum_height=self.chat_area.setter('height'))
        self.scroll = ScrollView(size_hint=(1,0.9), pos_hint={"top":1})
        self.scroll.add_widget(self.chat_area)
        root.add_widget(self.scroll)

        # Pastki qator
        self.bottom = BoxLayout(size_hint=(1,None), height=dp(60), padding=5, spacing=5, pos_hint={"x":0, "y":0})
        self.msg_input = TextInput(hint_text="Xabar yozing...", multiline=False, size_hint_x=0.8)

        # PNG tugma
        send_btn = Button(size_hint_x=0.2, background_normal="send_icon.png", background_down="send_icon.png")
        send_btn.bind(on_press=self.send_msg)

        self.bottom.add_widget(self.msg_input)
        self.bottom.add_widget(send_btn)
        root.add_widget(self.bottom)

        self.add_widget(root)

        # Xabarlarni avtomatik yangilash
        Clock.schedule_interval(self.fetch_messages, 2)  # har 2 soniyada yangilanadi

    def set_user(self,user):
        self.user = user

    def send_msg(self,instance):
        text = self.msg_input.text.strip()
        if text:
            # Firebase ga yuborish
            data = {"user": self.user, "text": text}
            try:
                requests.post(DB_URL, json=data)
            except Exception as e:
                print("Xatolik yuborishda:", e)
            
            # UI ga qo‘shish
            self.add_message(self.user, text, is_me=True)
            self.msg_input.text = ""
            self.scroll.scroll_y = 0

    def fetch_messages(self, dt):
        try:
            response = requests.get(DB_URL)
            messages = response.json()
            self.chat_area.clear_widgets()
            if messages:
                for key, val in messages.items():
                    user = val.get("user","")
                    text = val.get("text","")
                    is_me = (user == self.user)
                    self.add_message(user, text, is_me)
        except Exception as e:
            print("Xabarlarni olishda xatolik:", e)

    def add_message(self,user,text,is_me=False):
        box = BoxLayout(size_hint_y=None, padding=(10,5))
        max_width = Window.width*0.7

        lbl = Label(text="[b]{}:[/b] {}".format(user,text), markup=True, size_hint=(None,None),
                    halign="left", valign="middle", text_size=(max_width,None), color=(1,1,1,1))
        lbl.bind(texture_size=lambda inst,val: setattr(inst,'size',val))

        if is_me:
            box.add_widget(BoxLayout())
            box.add_widget(lbl)
        else:
            box.add_widget(lbl)
            box.add_widget(BoxLayout())

        self.chat_area.add_widget(box)

class ChatApp(App):
    def build(self):
        Window.softinput_mode = "below_target"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ChatScreen(name="chat"))
        return sm

if __name__=="__main__":
    ChatApp().run()