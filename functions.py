import cv2
import numpy as np
from PIL import Image
import pytesseract
from datetime import datetime

def removeCharsUnexpected(text):
    chars = text.split('\n')
    chars = chars[len(chars) - 1].upper()
    return ''.join(filter(str.isalnum, chars))

def numbersValid(text):
    number = text.strip()
    return ''.join([i for i in number if i.isdigit()])

def charsValid(text):
    chars = text.strip()
    return ''.join([i for i in chars if not i.isdigit()])

def validatePlate(text):
    text = text.strip()
    text.replace(' ', '')
    if len(text) == 7:
        chars = text[0:3]
        number = text[3:7]
    elif len(text) == 8:
        chars = text[0:3]
        number = text[4:8]
    else:
        return None
    
    if chars and number:
        number = numbersValid(number)
        chars = charsValid(chars)

        if len(chars) == 3 and len(number) == 4:
            string = chars+'-'+str(number)
            return string
    return None

def recognition(img, value):

    try:
        img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    except:
        return '', img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #img = cv2.bilateralFilter(img, 11, 75, 75) - 24/1
    img = cv2.bilateralFilter(img, 11, 75, 75)# - 26/01
    #img = cv2.bilateralFilter(img, 5, 9, 9) - 23
    #img = cv2.bilateralFilter(img, 9, 15, 15)

    ret, img = cv2.threshold(img, value, 255, cv2.THRESH_BINARY)

    #img = cv2.GaussianBlur(img, (5, 5), 0) - 23
    #img = cv2.GaussianBlur(img, (15, 15), 45) - 20
    #img = cv2.GaussianBlur(img, (11, 11), 31) - 23
    #img = cv2.GaussianBlur(img, (5, 5), 5) - 23
    #img = cv2.GaussianBlur(img, (11, 11), 75) - 24/1
    img = cv2.GaussianBlur(img, (11, 11), 75)# - 26/01
    #img = cv2.GaussianBlur(img, (5, 5), 75)

    cv2.imwrite('last_image_processed.jpg', img)

    image = Image.open('last_image_processed.jpg')

    res = pytesseract.image_to_string(image, lang='pubg')

    text = ''
    if len(res) > 0:
        chars = removeCharsUnexpected(res)
        text = validatePlate(chars)
        #if text:
            #print('Result', chars, value, text)

    return text, img
