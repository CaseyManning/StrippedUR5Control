import numpy as np
from keras.models import load_model
import tensorflow as tf
import threading
import atexit
import cv2
import random
import time

categories = ['flip', 'stir', 'noegg']
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

crop_size = (180, 320)

cap = None

model = None

recent_predictions = []

prediction = None

prediction_seconds = 5 #how many seconds in the past we use predictions from, 5 gives ~40 frames on my laptop

def startClassificationThread():
    print('starting egg classification thread')
    thread = threading.Thread(target=classificationThread, daemon=True)
    thread.start()

def classificationThread():
    print('egg classification thread started')
    global cap
    global prediction_seconds
    global model
    cap = cv2.VideoCapture(0)
    model = load_model('eggModel.h5')
    print('model loaded')
    global prediction
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    dt = 0
    lt = time.time()
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame, (1280, 720))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            temp_prediction = predict(frame, False, False)
            dt = time.time() - lt
            lt = time.time()
            recent_predictions.append(temp_prediction)
            print(temp_prediction)
            if len(recent_predictions) > prediction_seconds/dt:
                recent_predictions.pop(0)
                prediction = max(set(recent_predictions), key=recent_predictions.count)
        else: 
            raise Exception
            break
    print('cap closed bro')

def getPrediction():
    print(prediction)
    return prediction
 
def exit_handler():
    if cap is not None:
        cap.release()

atexit.register(exit_handler)

def predict(img=None, cropped=True, preprocessed=True):
    if not cropped:
        img = crop_center(img, *crop_size)
    if not preprocessed:
        img = img.astype('float32')
        img /= 255
    pred = model.predict([[img]])
    maxVal = max(pred[0])
    return categories[np.where(pred[0] == maxVal)[0][0]]

def crop_center(img,cropx,cropy):
    x,y,_ = img.shape
    startx = x//2-(cropx//2)+100
    starty = y//2-(cropy//2)    
    return img[startx:startx+cropx,starty:starty+cropy]

if __name__ == "__main__":
    # cap = cv2.VideoCapture(0)
    # ret, frame = cap.read()
    # frame = crop_center(frame, *crop_size)
    # print(predict(frame))
    startClassificationThread()
    while True:
        # if len(recent_predictions) > 0:
        #     print(recent_predictions[len(recent_predictions) - 1])
        pass
