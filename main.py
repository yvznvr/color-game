from random import randint
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.properties import ObjectProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import ScreenManager, Screen
from copy import copy


def callback(instance):
    print(instance.background_color, instance.id)


def getcolor():
    color = []
    for i in range(4):
        num = randint(1, 9)
        num = '.' + str(num)
        color.append(float(num))
    return color


def changecolor(color):
    newcolor = copy(color)
    newcolor[3] = color[3] - .05
    return newcolor


class MyWidget(Screen):
    grid = ObjectProperty(None)
    skor = ObjectProperty(None)


class StartScreen(Screen):
    pass


class Manager(ScreenManager):
    my_game = ObjectProperty(None)
    start_screen = ObjectProperty(None)


class MyApp(App):
    title = 'Farklı Olanı Bul'

    def check(self, instance):
        if str(self.right) == instance.id:
            self.skor += 10 * self.box
            self.counter += 1
            self.sm.my_game.skor.text = '[color=000000]Skor:{}[/color]'.format(
                self.skor)
            self.game()
        else:
            content = GridLayout(cols=1, rows=2)
            content.add_widget(Label(text='Skor: {}'.format(self.skor)))
            self.pop = Popup(title='Oyun Bitti', content=content, size_hint=(None,None), size=(250,250), auto_dismiss=False)
            content.add_widget(Button(text='Tamam', on_press=self.reset))
            self.pop.open()
            self.game()

    def game(self):
        self.sm.my_game.grid.clear_widgets()
        color = getcolor()
        self.sm.my_game.skor.text = '[color=000000]Skor:{}[/color]'.format(self.skor)
        if self.counter >= 9:
            self.box += 1
            self.counter = 0
        if self.counter < 0 and self.box > 3:
            self.box -= 1
            self.counter = 0
        box2 = self.box**2
        self.right = randint(0, box2 - 1)
        self.sm.my_game.grid.cols = self.box
        self.sm.my_game.grid.rows = self.box
        for i in range(box2):
            if i == self.right:
                self.sm.my_game.grid.add_widget(Button(id=str(
                    i), font_size=24, background_color=changecolor(color), on_press=self.check))
                continue
            else:
                self.sm.my_game.grid.add_widget(
                    Button(on_press=self.check, font_size=24, background_color=color))
                continue

    def start(self):
        self.sm.current = 'game'
        self.game()

    def reset(self, event):
        self.pop.dismiss()
        self.counter = 0
        self.skor = 0
        self.box = 3
        self.sm.current = 'menu'

    def build(self):
        self.sm = Manager()
        Window.clearcolor = (1, 1, 1, 1)
        self.mywidget = MyWidget()
        self.menu = StartScreen()
        self.counter = 0
        self.skor = 0
        self.box = 3
        return self.sm


if __name__ == '__main__':
    MyApp().run()
