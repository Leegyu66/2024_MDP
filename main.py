import cv2
import threading
from guizero import App, PushButton, Drawing, Box, Text
import tkinter as tk
import time
import os

# 카메라 피드를 읽고 창에 표시하는 플래그
root_dir = './animal'
animal_list = os.listdir(root_dir)
for i, animal in enumerate(animal_list):
    animal_list[i] = os.path.join(root_dir, animal)

print(animal_list)
stop_thread = False

# 카메라 피드를 읽고 창에 표시하는 함수

# thread 1
def show_camera_feed():
    img = cv2.imread(animal_list[1])  # 카메라 피드를 열기
    global stop_thread


    cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

    while not stop_thread:
        
        cv2.imshow("Camera Feed", img)  # 프레임을 OpenCV 창에 표시

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 누르면 종료
            stop_thread = True
            break
    
    cv2.destroyAllWindows()  # OpenCV 창 닫기
# 카메라 피드를 읽는 스레드 생성

# thread 2
def server():
    for i in range(10):
        count1 = 0
        print(count1)
        # time.sleep(1)

def server1():
    for i in range(10):
        count2 = 1
        print(count2)
        

# 스레드 저장
server_thread = threading.Thread(target=server)
camera_thread = threading.Thread(target=show_camera_feed)
server2_thread = threading.Thread(target=server1)

# OpenCV 스레드, 서버 스레드 시작
server_thread.start()
camera_thread.start()
server2_thread.start()

# GUI를 생성하고 버튼으로 프로그램을 종료하는 함수
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        # 그리기 영역 생성
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        # 도구 선택 영역 생성
        self.tool_frame = tk.Frame(root, bg="white")
        self.tool_frame.pack(pady=10)

        # 그리기 도구 버튼 생성
        self.line_button = tk.Button(self.tool_frame, text="직선", command=self.draw_line)
        self.line_button.pack(side="left", padx=10)

        self.rect_button = tk.Button(self.tool_frame, text="사각형", command=self.draw_rectangle)
        self.rect_button.pack(side="left", padx=10)

        self.oval_button = tk.Button(self.tool_frame, text="원", command=self.draw_oval)
        self.oval_button.pack(side="left", padx=10)

        # 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # 현재 그리기 정보
        self.start_x, self.start_y = None, None
        self.current_shape = None

    def draw_line(self):
        self.current_shape = "line"

    def draw_rectangle(self):
        self.current_shape = "rectangle"

    def draw_oval(self):
        self.current_shape = "oval"

    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_draw(self, event):
        if self.start_x and self.start_y:
            if self.current_shape == "line":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y)
            elif self.current_shape == "rectangle":
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y)
            elif self.current_shape == "oval":
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y)

    def end_draw(self, event):
        self.start_x, self.start_y = None, None

root = tk.Tk()
app = PaintApp(root)
root.mainloop()


# # guizero GUI 시작
# create_gui()

# OpenCV 스레드 종료를 기다림
camera_thread.join()
