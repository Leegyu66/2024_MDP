import speech_recognition as sr
# from playsound import playsound
import pygame

# Recognizer 객체 생성
r = sr.Recognizer()

# 마이크를 오디오 소스로 사용
mic = sr.Microphone()

# 저장할 오디오 파일의 이름
file_name = "recorded_audio.wav"

pygame.init()

# 음성 녹음 함수
def record_audio():
    with mic as source:
        print("녹음 시작...")
        audio_data = r.listen(source)
        print(r.recognize_google(audio_data, language='ko-KR'))
        print("녹음 완료!")
        return audio_data

# 오디오 파일 재생 함수
def play_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("recorded_audio.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy()==True:
        continue
    pygame.quit()

if __name__ == "__main__":
    # 음성 녹음
    audio_data = record_audio()

    # 오디오 파일로 저장
    with open(file_name, "wb") as f:
        f.write(audio_data.get_wav_data())

    # 오디오 파일 재생
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy()==True:
        continue
    pygame.quit()