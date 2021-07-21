import os
import time
import shutil

import numpy as np
from PIL import Image

from tensorflow.keras.models import load_model


class Predictor:
    def __init__(self):
        self.model = load_model('digit_model_CNN')

    def predict(self,):
        img=Image.open('digit.png')
        img=img.resize((28,28))
        img=img.convert('L')
        arr=np.array(np.array(img))
        arr=np.reshape(arr,(1,28,28,1))
        data = arr/255
        pred=self.model.predict(data)
        ans=np.argmax(pred)
        return ans

    def wrong_prediction(self,digit):
        shutil.move('digit.png','wrong_predictions/'+str(digit)+' '+time.strftime("%Y%m%d-%H%M%S")+'.png')
