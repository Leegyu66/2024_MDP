savebutton = Button(frame, text="Save", fg = "red",command=save)

from PIL import ImageGrab
from tkinter import *

window = Tk()
canvas = None
x1, y1 = None, None

wp = 5

def save():
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    w = window.winfo_width() + x
    h = window.winfo_height() + y
    
    box = (x, y, w, h)
    img=ImageGrab.grab(box) #창의 크기만큼만 이미지저장
    saveas='capture.png'
    img.save(saveas)

