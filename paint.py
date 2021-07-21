import os
from gtts import gTTS 
from playsound import playsound

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from prediction import Predictor

class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs) 
        with self.canvas: 
            Color(0,0,0)
            self.rect = Rectangle(pos = self.center,size =(28,28)) 
            self.bind(pos = self.update_rect,size = self.update_rect) 
        self.model=Predictor()

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

    def speak(self,ans):
        language = 'en'
        text='The digit is '+str(ans)
        audio = gTTS(text=text, lang=language, slow=False) 
        audio.save("audio.mp3") 
        playsound('audio.mp3')

    def on_touch_up(self,touch):
        self.export_to_png('digit.png')
        wid=BoxLayout(orientation='vertical')
        popup=Popup(title='Recognized digit',content=wid,size_hint=(.5,.5),auto_dismiss=False)
        digit=str(self.model.predict())
        wid.add_widget(Label(text=digit ,font_size='60sp'))
        wid.add_widget(Label(text='Is the digit recognized correct?',font_size='20sp'))
        btns=BoxLayout(size_hint=(1,0.5))
        btns.add_widget(Button(text='YES',on_press=popup.dismiss))
        def on_enter(*ard):
            try:
                number=int(txt_box.text)
            except:
                print('not number')
            if number>=0 and number<=9:
                self.model.wrong_prediction(txt_box.text)
                popup.dismiss()
        txt_box=TextInput(text='',multiline=False,input_type='number',on_text_validate=on_enter)
        inp_wid=BoxLayout(size_hint=(1,0.5))
        inp_wid.add_widget((Label(text='Enter the correct digit:')))
        inp_wid.add_widget(txt_box)
        def no_btn(*arg):
            wid.add_widget(inp_wid)
            wid.remove_widget(btns)
            txt_box.focus=True
        btns.add_widget(Button(text='NO',on_release=no_btn))
        wid.add_widget(btns)
        popup.open()
        self.speak(digit)
        self.canvas.clear()
        
class MyPaintApp(App):

    def build(self):
        return MyPaintWidget()

    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    MyPaintApp().run()
