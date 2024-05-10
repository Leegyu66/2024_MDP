import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# 원형 이미지를 만드는 함수
def create_round_image(diameter, fill_color, outline_color, outline_width):
    img = Image.new("RGBA", (diameter, diameter), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, diameter, diameter), fill=fill_color, outline=outline_color, width=outline_width)
    return img

# tkinter 루트 윈도우 생성
root = tk.Tk()

# 원형 이미지를 생성
diameter = 100
fill_color = "lightblue"
outline_color = "blue"
outline_width = 2

round_image = create_round_image(diameter, fill_color, outline_color, outline_width)

# PhotoImage로 변환
round_image_tk = ImageTk.PhotoImage(round_image)

# Label에 원형 이미지 추가
label = tk.Label(root, image=round_image_tk)
label.pack(pady=20)

# 또는 Button에 원형 이미지 추가
button = tk.Button(root, image=round_image_tk)
button.pack(pady=20)

root.mainloop()
