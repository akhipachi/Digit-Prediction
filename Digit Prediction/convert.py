from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
img=Image.open('test.png')
img=img.resize((28,28))
img=img.convert('L')
arr=np.array(np.array(img))
#plt.imshow(arr,cmap='binary')
#plt.show()
from tensorflow.keras.models import model_from_json
file = open('json', 'r')
model_json = file.read()
file.close()
model = model_from_json(model_json)
model.load_weights('h5_file')
arr=np.reshape(arr,(1,784))
mean=np.mean(arr)
std=np.std(arr)
ep = 1e-10
data = (arr-mean)/(std + ep)
pred=model.predict(data)
ans=np.argmax(pred)
print(ans)

from gtts import gTTS 
import os 
language = 'en'
text='The answer is '+str(ans)
myobj = gTTS(text=text, lang=language, slow=False) 
myobj.save("welcome.mp3") 
#os.system("mpg321 welcome.mp3") 
from playsound import playsound
from tkinter import *
root = Tk()
var = StringVar()
label = Label( root, text=text, relief=RAISED )
label.config(font=("Courier", 44))
label.pack()
playsound('welcome.mp3')
root.mainloop()
correct=input('is that correct (y/n): ')
if correct=='n':
    number=input('enter the correct answer: ')
    y=np.array([0,0,0,0,0,0,0,0,0,0,])
    y[int(number)]=1
    model.fit(data,y)
    json_file = model.to_json()
    with open('./json', "w") as file:
        file.write(json_file)
    model.save_weights('h5_file')