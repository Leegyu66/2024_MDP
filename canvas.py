import tkinter as tk
from tkinter import PhotoImage
import cv2
import os

Photo = PhotoImage(file="animal/lion.jpg")


# 그림판을 위한 클래스
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        # 그리기 영역 생성
        self.canvas = tk.Canvas(root, bg="white", width=1000, height=680)
        self.canvas.pack()

        # 도구 선택 영역 생성
        self.tool_frame = tk.Frame(root, bg="white")
        self.tool_frame.pack(pady=10)

        # 그리기 도구 버튼 생성
        self.line_button = tk.Button(self.tool_frame, image=Photo, command=self.draw_black)
        self.line_button.pack(side="left", padx=10)

        self.rect_button = tk.Button(self.tool_frame, text="사각형", command=self.draw_red)
        self.rect_button.pack(side="left", padx=10)

        self.oval_button = tk.Button(self.tool_frame, text="원", command=self.draw_blue)
        self.oval_button.pack(side="left", padx=10)

        self.point_button = tk.Button(self.tool_frame, text="점", command=self.draw_green)
        self.point_button.pack(side="left", padx=10)

        self.point_button = tk.Button(self.tool_frame, text="점", command=self.draw_gray)
        self.point_button.pack(side="left", padx=10)

        # 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.drawing)  # 드래그할 때 이벤트
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # 현재 그리기 정보
        self.start_x, self.start_y = None, None
        self.current_shape = "point"  # 기본 도구를 점으로 설정
        self.current_color = "black"

    # 직선 도구 선택
    def draw_black(self):
        self.current_color = "black"

    # 빨간색 선택
    def draw_red(self):
        self.current_color = "red"

    # 사각형 도구 선택
    def draw_blue(self):
        self.current_color = "blue"

    # 원 도구 선택
    def draw_green(self):
        self.current_color = "green"

    # 점 도구 선택
    def draw_gray(self):
        self.current_color = "gray"

    # 마우스를 눌렀을 때
    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y

    # 드래그할 때
    def drawing(self, event):
        if self.current_shape == "point":  # 점이 이어지도록 선을 그리기
            # 이전 위치와 현재 위치를 선으로 연결
            self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y, fill=self.current_color, width=6
            )
        # 현재 위치를 새 시작점으로 업데이트
        self.start_x, self.start_y = event.x, event.y

    # 마우스를 놓았을 때
    def end_draw(self, event):
        # 여기서는 아무 작업도 하지 않음
        self.start_x, self.start_y = None, None


# 애플리케이션 시작
root = tk.Tk()
app = PaintApp(root)
root.mainloop()
