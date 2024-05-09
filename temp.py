import threading
import time

# 스레드 1: 카운트 다운
def countdown(name, count):
    while count > 0:
        print(f"{name} - Count: {count}")
        count -= 1
        time.sleep(1)  # 1초 대기

# 스레드 2: 간단한 작업 반복
def simple_task(name):
    for i in range(5):
        print(f"{name} - Task: {i}")
        time.sleep(0.5)  # 0.5초 대기

# 두 스레드 생성
t1 = threading.Thread(target=countdown, args=("Thread 1", 5))
t2 = threading.Thread(target=simple_task, args=("Thread 2",))

# 스레드 시작
t1.start()
t2.start()

# 메인 스레드가 다른 스레드가 끝날 때까지 기다리도록 함
t1.join()
t2.join()

print("Both threads have finished.")
