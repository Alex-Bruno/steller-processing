import cv2
import dlib
import numpy as np
import imagezmq
import requests
from datetime import datetime
import copy
#
from functions import recognition
from env import getUrl

#
imageHub = imagezmq.ImageHub()
# detectors
detector = dlib.simple_object_detector("detector/484_imglab.svm")
#detectorPoints = dlib.shape_predictor("detector/plate.dat")
# Last plate
lastText = ''
diff = 0
lastTimestamp = datetime.timestamp(datetime.now())
# Start controller
while True:
    (rpiName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')

    objects = detector(frame, 2)

    timestamp = datetime.timestamp(datetime.now())
    start = datetime.timestamp(datetime.now())
    diff = timestamp - lastTimestamp
    valueText = None
    for detected in objects:

        left, top, right, bottom = (
        int(detected.left()), int(detected.top()), int(detected.right()), int(detected.bottom()))

        roi = frame[top: bottom, left: right]

        if np.shape(roi) != ():
            lastTimestamp = timestamp
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            textsDetected = []
            for val in [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]:
                text, img = recognition(roi, val)

                if text and len(text) > 3:
                    textsDetected.append(text)

            quantityMax = 0
            textMax = None
            for item in textsDetected:
                quantity = textsDetected.count(item)
                if quantity >= quantityMax:
                    quantityMax = quantity
                    textMax = copy.copy(item)
            valueText = copy.copy(textMax)
  
    if valueText and len(valueText) > 3 and valueText != 'Not Detected':
        if int(diff) > 5 or lastText != valueText:
            url = getUrl() + '/save-access/'
            requests.post(url, data=[('plate', str(valueText).strip())])
            lastText = valueText
            valueText = None

