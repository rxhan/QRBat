import traceback

import PIL.ImageOps
from PIL import Image

from pyzbar.pyzbar import decode
import os

from pyzbar.pyzbar import ZBarSymbol


def testing():
    path = '../uploads'
    files = os.listdir(path)
    for file in files:
        filename = os.path.join(path, file)
        read(filename)


def read(filename):
    result = []
    if os.path.isfile(filename):
        data = []
        print('testing', filename)
        img = Image.open(filename)
        try:
            data = decode(img, symbols=[ZBarSymbol.QRCODE])
            if not data:
                print('inverting image')
                iimg = PIL.ImageOps.invert(img)

                data = decode(iimg, symbols=[ZBarSymbol.QRCODE])
        except:
            data = []

        for code in data:
            read = bytes.decode(code.data)
            x,y,w,h = code.rect
            newimg = img.crop((x,y,x+w,y+h))
            result.append({'text': read, 'image': newimg})

    return result

#testing()