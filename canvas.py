import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import os
import requests
import base64
from datetime import datetime

url = "https://22b8-34-143-229-134.ngrok-free.app"

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

        # 색상 아이콘 생성
        self.color_black_icon = ImageTk.PhotoImage(self.create_round_image(50, "black", "black", 2))
        self.color_red_icon = ImageTk.PhotoImage(self.create_round_image(50, "red", "red", 2))
        self.color_blue_icon = ImageTk.PhotoImage(self.create_round_image(50, "blue", "blue", 2))
        self.color_yellow_icon = ImageTk.PhotoImage(self.create_round_image(50, "yellow", "yellow", 2))
        self.color_green_icon = ImageTk.PhotoImage(self.create_round_image(50, "green", "green", 2))
        self.color_gray_icon = ImageTk.PhotoImage(self.create_round_image(50, "gray", "gray", 2))

        # 아이콘 이미지 로드
        self.eraser_icon = ImageTk.PhotoImage(Image.open("icon/eraser.png").resize((50, 50)))
        self.whiteBoard_icon = ImageTk.PhotoImage(Image.open("icon/white_board.png").resize((50, 50)))
        self.save_icon = ImageTk.PhotoImage(Image.open("icon/save.png").resize((50, 50)))

        # 색상 선택 버튼 배치
        self.label_black = tk.Label(color_frame, image=self.color_black_icon)
        self.label_black.pack(side=tk.LEFT, padx=5)
        self.label_black.bind("<Button-1>", self.draw_black)

        self.label_red = tk.Label(color_frame, image=self.color_red_icon)
        self.label_red.pack(side=tk.LEFT, padx=5)
        self.label_red.bind("<Button-1>", self.draw_red)

        self.label_blue = tk.Label(color_frame, image=self.color_blue_icon)
        self.label_blue.pack(side=tk.LEFT, padx=5)
        self.label_blue.bind("<Button-1>", self.draw_blue)

        self.label_yellow = tk.Label(color_frame, image=self.color_yellow_icon)
        self.label_yellow.pack(side=tk.LEFT, padx=5)
        self.label_yellow.bind("<Button-1>", self.draw_yellow)

        self.label_green = tk.Label(color_frame, image=self.color_green_icon)
        self.label_green.pack(side=tk.LEFT, padx=5)
        self.label_green.bind("<Button-1>", self.draw_green)

        self.label_gray = tk.Label(color_frame, image=self.color_gray_icon)
        self.label_gray.pack(side=tk.LEFT, padx=5)
        self.label_gray.bind("<Button-1>", self.draw_gray)

        # 지우개 아이콘 배치
        self.label_eraser = tk.Label(color_frame, image=self.eraser_icon)
        self.label_eraser.pack(side=tk.LEFT, padx=5)
        self.label_eraser.bind("<Button-1>", self.eraser)

        # 화이트 보드 아이콘 배치
        self.label_whiteBoard = tk.Label(color_frame, image=self.whiteBoard_icon)
        self.label_whiteBoard.pack(side=tk.LEFT, padx=5)
        self.label_whiteBoard.bind("<Button-1>", self.clear_canvas)

        # 캔버스 캡쳐용 버튼 배치
        self.label_save = tk.Label(color_frame, image=self.save_icon)
        self.label_save.pack(side=tk.LEFT, padx=10)
        self.label_save.bind("<Button-1>", self.save_img)

        # 그림판 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.drawing)  # 드래그할 때 이벤트
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # 현재 그리기 정보
        self.start_x, self.start_y = None, None
        self.current_state = "draw"  # 기본 도구를 점으로 설정
        self.current_color = "black"
        self.prevPoint = [0, 0]
        self.currentPoint = [0, 0]

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

    # 노란색 선택
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

    # 캔버스 지우기
    def clear_canvas(self, event):
        self.canvas.delete("all")

    # 이미지 저장 함수
    def save_img(self, event):
        # 현재 날짜와 시간을 가져옴
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 파일 경로 설정
        img_dir = "user_img/user_img"
        png_dir = "user_img/ai_img"
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        if not os.path.exists(png_dir):
            os.makedirs(png_dir)

        img_path = os.path.join(img_dir, f"img_{current_time}.ps")
        png_path = os.path.join(img_dir, f"img_{current_time}.png")

        # 캔버스 내용을 PostScript 파일로 저장
        self.canvas.postscript(file=img_path)

        # PostScript 파일을 PNG로 변환
        with Image.open(img_path) as img:
            img.save(png_path)

        # 서버로 이미지 전송
        with open(png_path, 'rb') as file:
            files = {'file': file}
            data = {'name': "giraffe"}
            response = requests.post(url, files=files, data=data)

        # 서버 응답 처리
        if response.status_code == 200:
            response_data = response.json()
            encoded_image = response_data.get('encoded_image')

            if encoded_image:
                # Base64 인코딩된 이미지를 디코딩하여 저장
                img_data = base64.b64decode(encoded_image)
                if not os.path.exists(png_dir):
                    os.makedirs(png_dir)
                result_image_path = os.path.join(png_dir, f"result_image_{current_time}.png")
                with open(result_image_path, 'wb') as result_file:
                    result_file.write(img_data)

                print(f"Image successfully received and saved as {result_image_path}")
            else:
                print("No encoded image found in the response")
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)

    # 마우스를 눌렀을 때
    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y

    # 드래그할 때
    def drawing(self, event):
        x, y = event.x, event.y
        self.currentPoint = [x, y]

        if self.current_state == "draw" and self.prevPoint != [0, 0]:  # 점이 이어지도록 선을 그리기
            # 이전 위치와 현재 위치를 선으로 연결
            self.canvas.create_line(
                self.prevPoint[0], self.prevPoint[1], self.currentPoint[0], self.currentPoint[1], fill=self.current_color, width=10
            )
        self.prevPoint = self.currentPoint

        if self.current_state == "erase":
            self.canvas.create_oval(
                event.x-15, event.y-15, event.x+15, event.y+15, fill="white", outline="white"
            )

    # 마우스를 놓았을 때
    def end_draw(self, event):
        self.start_x, self.start_y = None, None
        self.prevPoint = [0, 0]

    # 동그라미 그리기
    def create_round_image(self, diameter, fill_color, outline_color, outline_width):
        img = Image.new("RGBA", (diameter+5, diameter+5), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, diameter, diameter), fill=fill_color, outline=outline_color, width=outline_width)
        return img

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
