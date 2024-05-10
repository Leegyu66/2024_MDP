import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
import cv2
import os

# 그림판을 위한 클래스
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        # 그리기 영역 생성
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # 색상 선택을 위한 프레임
        color_frame = tk.Frame(root)
        color_frame.pack(side=tk.TOP)
        
        # 색상 선택 버튼 배치
        self.label_black = tk.Label(color_frame, image=color_black_icon)
        self.label_black.pack(side=tk.LEFT, padx=5)

        self.label_red = tk.Label(color_frame, image=color_red_icon)
        self.label_red.pack(side=tk.LEFT, padx=5)

        self.label_blue = tk.Label(color_frame, image=color_blue_icon)
        self.label_blue.pack(side=tk.LEFT, padx=5)

        self.label_yellow = tk.Label(color_frame, image=color_yellow_icon)
        self.label_yellow.pack(side=tk.LEFT, padx=5)

        self.label_green = tk.Label(color_frame, image=color_green_icon)
        self.label_green.pack(side=tk.LEFT, padx=5)

        self.label_gray = tk.Label(color_frame, image=color_gray_icon)
        self.label_gray.pack(side=tk.LEFT, padx=5)

        self.label_eraser = tk.Label(color_frame, image=eraser_icon)
        self.label_eraser.pack(side=tk.LEFT, padx=5)

        # 그림판 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.drawing)  # 드래그할 때 이벤트
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # 색상 선택 이벤트 바인딩
        self.label_black.bind("<Button-1>", self.draw_black)
        self.label_red.bind("<Button-1>", self.draw_red)
        self.label_blue.bind("<Button-1>", self.draw_blue)
        self.label_yellow.bind("<Button-1>", self.draw_yellow)
        self.label_green.bind("<Button-1>", self.draw_green)
        self.label_gray.bind("<Button-1>", self.draw_gray)
        self.label_eraser.bind("<Button-1>", self.eraser)

        # 현재 그리기 정보
        self.start_x, self.start_y = None, None
        self.current_state = "draw"  # 기본 도구를 점으로 설정
        self.current_color = "black"

    # 검은색 선택
    def draw_black(self, event):
        self.current_color = "black"
        self.current_state = "draw"

    # 빨간색 선택
    def draw_red(self, event):
        self.current_color = "red"
        self.current_state = "draw"

    # 파란색 선택
    def draw_blue(self, event):
        self.current_color = "blue"
        self.current_state = "draw"

    def draw_yellow(self, event):
        self.current_color = "yellow"
        self.current_state = "draw"

    # 초록색 선택
    def draw_green(self, event):
        self.current_color = "green"
        self.current_state = "draw"

    # 회색 선택
    def draw_gray(self, event):
        self.current_color = "gray"
        self.current_state = "draw"

    # 지우개 선택
    def eraser(self, event):
        self.current_state = "erase"

    # 마우스를 눌렀을 때
    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y

    # 드래그할 때
    def drawing(self, event):
        if self.current_state == "draw":  # 점이 이어지도록 선을 그리기
            # 이전 위치와 현재 위치를 선으로 연결
            self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y, fill=self.current_color, width=6
            )
        # 현재 위치를 새 시작점으로 업데이트
        self.start_x, self.start_y = event.x, event.y

        if self.current_state == "erase"

    # 마우스를 놓았을 때
    def end_draw(self, event):
        # 여기서는 아무 작업도 하지 않음
        self.start_x, self.start_y = None, None

# 동그라미 그리기
def create_round_image(diameter, fill_color, outline_color, outline_width):
    img = Image.new("RGBA", (diameter+5, diameter+5), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, diameter, diameter), fill=fill_color, outline=outline_color, width=outline_width)
    return img

# 애플리케이션 시작
root = tk.Tk()

# 아이콘 불러오기
color_black_icon = ImageTk.PhotoImage(create_round_image(50, "black", "black", 2))
color_red_icon = ImageTk.PhotoImage(create_round_image(50, "red", "red", 2))
color_blue_icon = ImageTk.PhotoImage(create_round_image(50, "blue", "blue", 2))
color_yellow_icon = ImageTk.PhotoImage(create_round_image(50, "yellow", "yellow", 2))
color_green_icon = ImageTk.PhotoImage(create_round_image(50, "green", "green", 2))
color_gray_icon = ImageTk.PhotoImage(create_round_image(50, "gray", "gray", 2))
eraser_icon = ImageTk.PhotoImage(Image.open("icon/eraser.png").resize((100, 100)))

# 애플리케이션 시작
app = PaintApp(root)
root.mainloop()
