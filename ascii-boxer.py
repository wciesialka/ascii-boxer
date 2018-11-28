from PIL import Image
import os
from math import floor

R,G,B = 0,1,2
MAX_WH = 64 

def get_file_path():
    path = input("Image to translate: ")
    if(os.path.isfile(path)):
        return path
    else:
        print("File does not exist.")
        return get_file_path()

def get_image():
    try:
        img = Image.open(get_file_path())
    except:
        print("File is not an image.")
        return get_image()
    else:
        return img

def resize_if_needed(img):
    size = img.size
    w, h = size[0], size[1]
    compare = max(w,h)
    if (compare > MAX_WH):
        ratio = MAX_WH/compare
        new_w, new_h = floor(w*ratio), floor(h*ratio)
        return img.resize((new_w,new_h), Image.ANTIALIAS)
    else:
        return img

def val_to_char(val):
    v = val/255
    if v <= 0.2:
        return ' '
    elif v > 0.2 and v <= 0.4:
        return '\u2591'
    elif v > 0.4 and v <= 0.6:
        return '\u2592'
    elif v > 0.6 and v <= 0.8:
        return '\u2593'
    else:
        return '\u2588'

def main():
    img = get_image()
    img = resize_if_needed(img).convert(mode="HSV")
    size = img.size
    w,h = size
    for y in range(h):
        for x in range(w):
            px = img.getpixel((x,y))
            hue,sat,val = px
            print(val_to_char(val),end='')
        print("")

if __name__=="__main__":
    main()
