from PIL import Image
import os
from math import floor
import re

R,G,B = 0,1,2
MAX_WH = 70 # a little less than the typical max cpl

def get_file_path():
    path = input("Image to translate: ")
    if(os.path.isfile(path)):
        return path
    else:
        print("File does not exist.")
        return get_file_path()

def get_image():
    filepath = get_file_path()
    try:
        img = Image.open(filepath)
    except:
        print("File is not an image.")
        return get_image()
    else:
        return img, filepath

def resize_if_needed(img,desired_width=MAX_WH):
    size = img.size
    w, h = size[0], size[1]
    if (w > desired_width):
        ratio = desired_width/w
        new_w, new_h = floor(w*ratio), floor(h*ratio)
        return img.resize((new_w,new_h), Image.ANTIALIAS)
    else:
        return img

CHARS = (' ','\u2591','\u2592','\u2593','\u2588')

def val_to_char(val,invert=False):
    v = val/255
    if invert:
        v = 1 - v
    if v <= 0.2:
        return CHARS[4]
    elif v > 0.2 and v <= 0.4:
        return CHARS[3]
    elif v > 0.4 and v <= 0.6:
        return CHARS[2]
    elif v > 0.6 and v <= 0.8:
        return CHARS[1]
    else:
        return CHARS[0]

def get_yn():
    i = input("[Y/N] ").lower()
    if i == 'y' or i=='yes' or i == 't' or i == 'true' or i == 'ye':
        return True
    elif i =='n' or i=='no' or i == 'f' or i == 'false':
        return False
    else:
        print("Please enter Y for 'Yes' or N for 'No'")
        return get_invert()

def get_line_width():
    try:
        i = int(input("Maximum line width: "))
    except:
        print("Must be an integer.")
        return get_line_width()
    else:
        if i <= 0:
            print("Must be greater than zero.")
            return get_line_width()
        else:
            return i

def write_to_file(text,fallback_filename="ascii-art"):
    fn = input("File path: ")
    if fn.endswith("/") or fn.endswith("\\") or fn.endswith(" "):
        fn += fallback_filename
    if not fn.endswith(".txt"):
        fn += ".txt"
    REGEX = "(?!)(^\/$|(^(?=\/)|^\.|^\.\.|^\~|^\~(?=\/))(\/(?=[^/\0])[^/\0]+)*\/?$)"
    fn = re.sub(REGEX,'',fn)
    fn = os.path.normpath(fn)
    if os.path.exists(fn):
        print("File exists. Overwrite?")
        can_write = get_yn()
    else:
        d = os.path.dirname(fn)
        if not os.path.exists(d):
            try:
                os.makedirs(d)
            except:
                print("Could not make directories to that path.")
                can_write = False
            else:
                can_write = True
        else:
            can_write = True
    if can_write:
        try:
            f = open(fn,"w")
        except:
            print("Could not create or open file for writing. Check permissions and try again.")
            write_to_file(text,fallback_filename)
        else:
            try:
                f.write(text)
            except:
                print("Could not write to file. Try again.")
                write_to_file(text,fallback_filename)
            else:
                print(f"Successfully wrote to file {fn}")
            finally:
                f.close()
    else:
        print("Could not write to file. Try again.")
        write_to_file(text,fallback_filename)


def main():
    img, fbfn = get_image()
    fbfn = os.path.basename(fbfn)
    fbfn = fbfn[:fbfn.rfind(".")]
    line_width = get_line_width()
    img = resize_if_needed(img,line_width).convert(mode="HSV")
    size = img.size
    w,h = size
    print("Invert colors? (Helps if text displayed is a light color on a dark background.)")
    invert = get_yn()
    s = ""
    for y in range(h):
        for x in range(w):
            px = img.getpixel((x,y))
            hue,sat,val = px
            s += val_to_char(val,invert=invert)
        if y < h-1:
            s += os.linesep
    print(s)
    print("Write to file?")
    if get_yn():
        with open("test.txt","w") as f:
            write_to_file(s,fallback_filename=fbfn)

if __name__=="__main__":
    main()
