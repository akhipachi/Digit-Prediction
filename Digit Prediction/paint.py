from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.button import Button
import os


class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs) 
        with self.canvas: 
            Color(0,0,0)
            self.rect = Rectangle(pos = self.center,size =(28,28)) 
            self.bind(pos = self.update_rect,size = self.update_rect) 
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size 

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1,1,1)
            d = 30.
            #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y),width=15)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

    def on_touch_up(self,touch):
        self.export_to_png('test.png')
        MyPaintApp().stop()
        
class MyPaintApp(App):

    def build(self):
        
        return MyPaintWidget()

    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    MyPaintApp().run()

import convert
