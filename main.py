import cv2
import numpy as np
import threading
import tkinter as tk
import time
from PIL import ImageTk, Image, ImageDraw, ImageGrab
import cv2
import os
from random import randint, uniform
import serial
# import playsound
# from canvas import PaintApp
import pygame
import numpy as np
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
import speech_recognition as sr
import requests
import subprocess
import pyaudio
import wave
import urllib3
import json
import base64
import os
import datetime
from Timeout import timeout

ser = serial.Serial(
    port='/dev/ttyAMA0',  # 라즈베리 파이의 기본 시리얼 포트
    baudrate=115200,        # 보드레이트는 필요에 따라 변경
    timeout=1             # 타임아웃 설정 (초)
)

# 얼굴인식 초기설정
serial_number = 0

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = 'face_recog/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

# model = SentenceTransformer('jhgan/ko-sroberta-multitask')

names = ['kkk', 'jihye', 'jimin']
animal_dict = {0:'곰', 1:'비버', 2:'고양이', 3:'코끼리', 4:'기린', 5:'사자', 6:'토끼'}
number_dict = {'곰':0, '비버':1, '고양이':2, '코끼리':3, '기린':4, '사자':5, '토끼':6}
korea_english = {'곰':'bear', '비버':'beaver', '고양이':'cat', '코끼리':'elephant', '기린':'giraffe', '사자':'lion', '토끼':'rabbit'}
real_encode = ''

# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# minW = 0.1 * cam.get(cv2.CAP_PROP_FRAME_WIDTH)
# minH = 0.1 * cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# 카메라 피드를 읽고 창에 표시하는 플래그
root_dir_img = './animal_img'
root_dir_audio = './recording_wav'
root_dir_reaction = './reaction'
root_dir_painting = './lets_painting'
animal_list = os.listdir(root_dir_img)
audio_list = os.listdir(root_dir_audio)
reaction_list = os.listdir(root_dir_reaction)
painting_list = os.listdir(root_dir_painting)


for i, animal in enumerate(animal_list):
    animal_list[i] = os.path.join(root_dir_img, animal)

for i, audio in enumerate(audio_list):
    audio_list[i] = os.path.join(root_dir_audio, audio)

for i, reaction in enumerate(reaction_list):
    reaction_list[i] = os.path.join(root_dir_reaction, reaction)

for i, painting in enumerate(painting_list):
    painting_list[i] = os.path.join(root_dir_painting, painting)

audio_list = sorted(audio_list)
animal_list = sorted(animal_list)
reaction_list = sorted(reaction_list)
painting_list = sorted(painting_list)

very_good_audio = audio_list.pop()
# start_drawing_img = animal_list.pop()

# 거의 필요없음
stop_thread = False

# opencv 플래그 
face_detect_flag = True  # 얼굴인식
cv2_init = True
animal_flag = False      # 동물표시
ai_paint_flag = False    # 애기 ai 이미지 표시
cam_flag = True

# thread 플래그
get_voice_flag = False
get_serial_flag = False

# 그림 그리기 플래그
start_drawing_flag = False

face_sequence = []
user_name = ''
ai_painting_path = 'user_img/ai_img'
audioFilePath = ''
accuracy = 0
reaction_number = 2

# 카메라 피드를 읽고 창에 표시하는 함수
print(animal_list)
def audio_output(path):
    pygame.mixer.init() 
    pygame.mixer.music.load(audio_list[serial_number])
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy()==True:
        continue
    pygame.quit()
    time.sleep(2)

def classifier_animal(data):
    data = data[-2:]
    try:
        if 21 < int(data) < 28:
            return "코끼리"
        elif int(data) == 30:
            return "기린"
        elif 33 < int(data) < 41:
            return "사자"
        elif 49 < int(data) < 58:
            return "비버"

    except:
        if "A" in data or "F" in data:
            return "곰"
        elif "B" in data:
            return "고양이"
        elif "C" in data:
            return "토끼"

    return data

def record_audio(file_path, record_seconds=2, sample_rate=44100, channels=1):
    chunk = 1024
    format = pyaudio.paInt16
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels,
                        rate=sample_rate, input=True,
                        frames_per_buffer=chunk)
    
    print("Recording...")
    frames = []
    
    for _ in range(0, int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Recording Finished")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

@timeout(10)
def send_to_etri_api(file_path, script):
    # 32a544d6-d365-4d08-a0cf-c7181e720166 # 지혜
    # e1187d66-df2e-45d1-b309-17068d8699c3 # 지민
    # 9c09c855-7ebc-49fc-b6a7-420259187237 # 남궁
    # c831eb52-6ffd-476a-b9b6-18f827070008 # 규영

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor"
    accessKey = "32a544d6-d365-4d08-a0cf-c7181e720166"
    languageCode = "korean"

    with open(file_path, "rb") as file:
        audioContents = base64.b64encode(file.read()).decode("utf8")

    requestJson = {
        "argument": {
            "language_code": languageCode,
            "script": script,
            "audio": audioContents
        }
    }

    http = urllib3.PoolManager()
    print("Start Evaluating")
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    print("[responseCode] " + str(response.status))
    print("[responBody]")
    response_data = json.loads(response.data.decode("utf8"))
    score = response_data['return_object']['score']
    print(f"발음 평가 점수: {score}")

    return score

# thread 1
def show_camera_feed():
    global user_name, face_detect_flag, serial_number, get_voice_flag, face_sequence, get_serial_flag, cv2_init, reaction_number, start_drawing_flag, ai_paint_flag, ai_painting_path, animal_flag, cam_flag    
    
    while not stop_thread:

        if cam_flag:
            print("cam flag is opened")
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

            minW = 0.1 * cam.get(cv2.CAP_PROP_FRAME_WIDTH)
            minH = 0.1 * cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

            cam_flag = False

        if face_detect_flag and cam.isOpened:
            ret, img = cam.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=6,
                minSize=(int(minW), int(minH))
            )

            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                if confidence < 55 :
                    id = names[id]
                    face_sequence.append(id)
                else:
                    id = "unknown"
                
                confidence = "  {0}%".format(round(100-confidence))

                cv2.putText(img,str(id), (x+5,y-5),font,1,(255,255,255),2)
                cv2.putText(img,str(confidence), (x+5,y+h-5),font,1,(255,255,0),1)
            
            cv2.imshow('camera',img)
            if len(face_sequence) > 3:
                if face_sequence[-1] == face_sequence[-2] == face_sequence[-3]:
                    user_name = face_sequence[-1]
                    face_detect_flag = False 
                    get_serial_flag = True
                    animal_flag = True
                    cv2_init = True
                    
                    # serial_thread.start()
                    cam.release()  

            if cv2.waitKey(1) == ord("q"):
                face_detect_flag = False 
                get_serial_flag = True
                animal_flag = True
                cv2_init = True
                user_name = "jimin"
                
                # serial_thread.start()
                cam.release()  

        elif animal_flag:
            
            if cv2_init:
                img = cv2.imread(reaction_list[reaction_number])
            elif start_drawing_flag:
                img = cv2.imread(painting_list[serial_number])
            else:
                img = cv2.imread(animal_list[serial_number])  # 카메라 피드를 열기
            # global stop_thread

            cv2.namedWindow("camera", cv2.WINDOW_NORMAL)

            cv2.imshow("camera", img)  # 프레임을 OpenCV 창에 표시

            

            if cv2.waitKey(100) & 0xFF == ord('q'):  # 'q' 누르면 종료
                break

        elif ai_paint_flag:
            img = cv2.imread(os.path.join('server', ai_painting_path))

            print(os.path.join('server', ai_painting_path))
            cv2.imshow("camera", img)

            cv2.namedWindow("camera", cv2.WINDOW_NORMAL)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
    
    cv2.destroyAllWindows()  # OpenCV 창 닫기        

def get_serial_number():
    global get_voice_flag, serial_number, get_serial_flag, real_encode, cv2_init, face_sequence
    data_sequence = []
    face_sequence = []
    print("Start read serial")
    # while True:
    #     if get_serial_flag:
    #         time.sleep(6)
    #         serial_number = randint(0, len(animal_list)-2)
    #         get_voice_flag = True
    #         get_serial_flag = False
    #         cv2_init = False
    #         voice_thread.start()
    #         # real_encode = model.encode(animal_dict[serial_number])
    #         break
    while True:
        # ser.open()
        if get_serial_flag:
            try:
                while True:
                    if ser.in_waiting > 0:
                        data = ser.readline().decode('utf-8').rstrip()
                        data = classifier_animal(data)
                        data_sequence.append(data)
                        if len(data_sequence) > 3:
                            if data != "rd" and data_sequence[-3] == data_sequence[-2] == data_sequence[-1]: 
                                serial_number = number_dict[data]
                                print(f"Received: {data}")
                                # real_encode = model.encode(animal_dict[serial_number])  
                                # voice_thread.start()
                                cv2_init = False
                                data_sequence = []
                                print("Stop serial thread")
                                break
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("Exiting Program")

            finally:
                ser.close()
                get_voice_flag = True
                get_serial_flag = False
                print("Start voice thread")
                get_voice()
                print("Finish voice thread")
    

def get_voice():
    global get_voice_flag, serial_number, real_encode, reaction_number, user_name, start_drawing_flag, cv2_init, accuracy, audioFilePath
    
    print("Start voice thread")
    
    flag = True

    if get_voice_flag:
        print("Start audio")
        for i in range(3):
            print("Serial number: ", serial_number)
            print("Audio_list: ", audio_list)
            audio_output(audio_list[serial_number])
        # audio_output()
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_folder = "audio_file"
        # if not os.path.exists(audio_folder):
        #     os.makedirs(audio_folder)
        
        audioFilePath = os.path.join(audio_folder, f"{current_time}.wav")
        script = animal_dict[serial_number]
        
        record_audio(os.path.join('server', audioFilePath), record_seconds=3)
        try:
            score = send_to_etri_api(os.path.join('server', audioFilePath), script)
        except:
            score = str(uniform(1, 2))
        score = float(score)
        accuracy = int(score/2*100)

        if accuracy > 100:
            reaction_number = 3
        elif accuracy > 35:
            reaction_number = 1
        else:
            reaction_number = 0

        cv2_init = True

        time.sleep(6)

        cv2_init = False
        start_drawing_flag = True
        get_voice_flag = False



##################################################################################################################
# 그림판
url_ai = "https://e365-35-186-153-205.ngrok-free.app"

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

        '''
        face_detect_flag = True  # 얼굴인식
        cv2_init = True
        animal_flag = False      # 동물표시
        ai_paint_flag = False    # 애기 ai 이미지 표시

        # thread 플래그
        get_voice_flag = False
        get_serial_flag = False

        # 그림 그리기 플래그
        start_drawing_flag = False
        '''
        global ai_painting_path, animal_flag, ai_paint_flag, cv2_init, face_detect_flag, get_voice_flag, get_serial_flag, start_drawing_flag, cam_flag, reaction_number
        # 현재 날짜와 시간을 가져옴
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(serial_number)

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
        self.canvas.postscript(file=os.path.join('server', img_path))

        # PostScript 파일을 PNG로 변환
        with Image.open(os.path.join('server', img_path)) as img:
            img.save(os.path.join('server', png_path))

        # 서버로 이미지 전송
        with open(os.path.join('server', png_path), 'rb') as file:
            files = {'file': file}
            data = {'name': korea_english[animal_dict[serial_number]]}
            response = requests.post(url_ai, files=files, data=data)

        # 서버 응답 처리
        if response.status_code == 200:
            print("responsed")
            response_data = response.json()
            encoded_image = response_data.get('encoded_image')

            if encoded_image:
                # Base64 인코딩된 이미지를 디코딩하여 저장
                img_data = base64.b64decode(encoded_image)
                if not os.path.exists(os.path.join('server', png_dir)):
                    os.makedirs(os.path.join('server', png_dir))
                result_image_path = os.path.join(png_dir, f"result_image_{current_time}.png")

                ai_painting_path = result_image_path

                with open(os.path.join('server', result_image_path), 'wb') as result_file:
                    result_file.write(img_data)

                print(f"Image successfully received and saved as {result_image_path}")


                animal_flag = False
                ai_paint_flag = True

                url = 'http://127.0.0.1:5000/upload_information'

                data = {
                'user_id':user_name,
                'product_audio':audioFilePath,
                'product_word':animal_dict[serial_number],
                'product_accuracy':accuracy,
                'product_image':png_path,
                'modify_image':ai_painting_path
                }
                response = requests.post(url, json=data)

                time.sleep(10)

                face_detect_flag = True  # 얼굴인식
                cv2_init = True
                animal_flag = False      # 동물표시
                ai_paint_flag = False    # 애기 ai 이미지 표시
                cam_flag = True

                # thread 플래그
                get_voice_flag = False
                get_serial_flag = False

                # 그림 그리기 플래그
                start_drawing_flag = False

                reaction_number = 2

                ser.open()
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

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = PaintApp(root)
#     root.mainloop()
################################################################################################################
                
                        


# 스레드 저장
# get_serial_number = threading.Thread(target=get_serial_number)
# voice_thread = threading.Thread(target=get_voice)
serial_thread = threading.Thread(target=get_serial_number)
camera_thread = threading.Thread(target=show_camera_feed)

# OpenCV 스레드, 서버 스레드 시작
serial_thread.start()
camera_thread.start()

# GUI를 생성하고 버튼으로 프로그램을 종료하는 함수


root = tk.Tk()

# 아이콘 불러오기

app = PaintApp(root)
root.mainloop()


# OpenCV 스레드 종료를 기다림
camera_thread.join()
serial_thread.join()