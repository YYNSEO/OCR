import socket
import cv2  # OpenCV

import tkinter  # Tkinter 및 GUI 관련
import tkinter as tk
import PIL.Image, PIL.ImageTk
import numpy as np
import threading  # Thread
import random

root = tk.Tk()
result_img = 0  # 전역변수로 최종 이미지를 받도록 했다
l = 20      # 파장(wave length)
amp = 15    # 진폭(amplitude)

def recvall(sock,count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)

    return buf



def streaming():
    HOST = "192.168.31.87"
    PORT = 9999
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    global result_img
    count = 0
    while True:
        message = '1'
        client_socket.send(message.encode())
        length = recvall(client_socket, 16)
        # print(length)
        stringData = recvall(client_socket, int(length))
        data = np.frombuffer(stringData, dtype='uint8')
        if count == 0:
            print(length, "len")
            print(stringData, "std")
            print(data)
            print(type(data))
            for i in data:
                count += 1
                print(i)
                print(count, ":c\n")
        decimg = cv2.imdecode(data, 1)
        result_img = decimg
    client_socket.close()

class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1600x900") #해상도 선언
        self.master.title("Streaming")
        self.delay = 15
        self.flags=0
        # View Video
        self.canvas = tkinter.Canvas(self.master, width=640, height=480)
        self.canvas.pack()
        self.label = tkinter.Label(self.master, width=20, height=5)
        self.label.pack()
        self.btn = tkinter.Button(self.label,text="오락실필터",width=20, height=5, command=self.change)
        self.btn.pack(side="left")
        self.btn2 = tkinter.Button(self.label,text="지그재그",width=20, height=5, command=self.flagschange)
        self.btn2.pack(side="left")
        self.btn3 = tkinter.Button(self.label,text="원본",width=20, height=5, command=self.flagchange)
        self.btn3.pack(side="left")
        self.entry = tkinter.Entry(self.master, width=30)
        self.entry.configure(font=("",12))
        self.entry.pack(pady=5, ipady=7)
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.func1)

        self.update()




    def flagschange(self):
        self.flags=2
    def flagchange(self):
        self.flags=0
    def change(self):
        self.flags = 1
    def update(self):
        global vid
        try:
            vid = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            #->필터함수호출
            #필터에서 리턴받은 결과 프레임
            if self.flags == 1:
                vid = self.filter(vid)
            if self.flags==2:
                vid=self.add(vid)

            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(vid))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        except:
            pass
        self.master.after(self.delay, self.update)

    def func1(self, e):
        vid2 = cv2.cvtColor(vid, cv2.COLOR_RGB2BGR)
        cv2.imwrite(f'{self.entry.get()}.png', vid2)




    def add(self, frame):

        #지그재그 함수
        rows, cols = frame.shape[:2]
        # 초기 매핑 배열 생성
        mapy, mapx = np.indices((rows, cols), dtype=np.float32)

        # sin, cos 함수를 적용한 변형 매핑 연산
        sinx = mapx + amp * np.sin(mapy / l)
        cosy = mapy + amp * np.cos(mapx / l)

        # 영상 매핑
        img_sinx = cv2.remap(frame, sinx, mapy, cv2.INTER_LINEAR)  # x축만 sin 곡선 적용
        img_cosy = cv2.remap(frame, mapx, cosy, cv2.INTER_LINEAR)  # y축만 cos 곡선 적용
        # x,y 축 모두 sin, cos 곡선 적용 및 외곽 영역 보정
        img_both = cv2.remap(frame, sinx, cosy, cv2.INTER_LINEAR, None, cv2.BORDER_REPLICATE)
        return img_both

        #늘리기 함수

        # height, width = frame.shape[:2]
        # scale_factor = 2
        # new_height = int(height * scale_factor)
        # delta = int((new_height - height) / 2)
        # stretched_frame = cv2.resize(frame, (width, new_height))
        # if delta > 0:
        #     stretched_frame = stretched_frame[delta:-delta, :]
        # return stretched_frame

        # 오목렌즈 함수

        # rows, cols = frame.shape[:2]
        #
        # # ---① 설정 값 셋팅
        # exp = 2  # 볼록, 오목 지수 (오목 : 0.1 ~ 1, 볼록 : 1.1~)
        # scale = 1  # 변환 영역 크기 (0 ~ 1)
        #
        # # 매핑 배열 생성 ---②
        # mapy, mapx = np.indices((rows, cols), dtype=np.float32)
        #
        # # 좌상단 기준좌표에서 -1~1로 정규화된 중심점 기준 좌표로 변경 ---③
        # mapx = 2 * mapx / (cols - 1) - 1
        # mapy = 2 * mapy / (rows - 1) - 1
        #
        # # 직교좌표를 극 좌표로 변환 ---④
        # r, theta = cv2.cartToPolar(mapx, mapy)
        #
        # # 왜곡 영역만 중심확대/축소 지수 적용 ---⑤
        # r[r < scale] = r[r < scale] ** (1/exp)
        #
        # # 극 좌표를 직교좌표로 변환 ---⑥
        # mapx, mapy = cv2.polarToCart(r, theta)
        #
        # # 중심점 기준에서 좌상단 기준으로 변경 ---⑦
        # mapx = ((mapx + 1) * cols - 1) / 2
        # mapy = ((mapy + 1) * rows - 1) / 2
        # # 재매핑 변환
        # distorted = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        # return distorted

        # 볼록렌즈 함수

        # rows, cols = frame.shape[:2]
        #
        # # ---① 설정 값 셋팅
        # exp = 2  # 볼록, 오목 지수 (오목 : 0.1 ~ 1, 볼록 : 1.1~)
        # scale = 1  # 변환 영역 크기 (0 ~ 1)
        #
        # # 매핑 배열 생성 ---②
        # mapy, mapx = np.indices((rows, cols), dtype=np.float32)
        #
        # # 좌상단 기준좌표에서 -1~1로 정규화된 중심점 기준 좌표로 변경 ---③
        # mapx = 2 * mapx / (cols - 1) - 1
        # mapy = 2 * mapy / (rows - 1) - 1
        #
        # # 직교좌표를 극 좌표로 변환 ---④
        # r, theta = cv2.cartToPolar(mapx, mapy)
        #
        # # 왜곡 영역만 중심확대/축소 지수 적용 ---⑤
        # r[r < scale] = r[r < scale] ** exp
        #
        # # 극 좌표를 직교좌표로 변환 ---⑥
        # mapx, mapy = cv2.polarToCart(r, theta)
        #
        # # 중심점 기준에서 좌상단 기준으로 변경 ---⑦
        # mapx = ((mapx + 1) * cols - 1) / 2
        # mapy = ((mapy + 1) * rows - 1) / 2
        # # 재매핑 변환
        # distorted = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        # return distorted

    def filter(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, src_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) #이진화로 바꿔줌 thresh : 임계값 maxval : 0보다 큰 값을 255로 바꿈 , 뒤에 있는 것이 효과

        contours, _ = cv2.findContours(src_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 외각선 찾기

        h, w = gray.shape[:2] #
        dst = np.zeros((h, w, 3), np.uint8) #h, w 만큼의 검은색 화면으로 channel 3만큼 생성, uint8은 양수만 표현 가능

        for i in range(len(contours)):
            c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # rgb 랜덤으로 주기
            cv2.drawContours(dst, contours, i, c, 1, cv2.LINE_AA) #선 그리기
        return dst






if __name__ == "__main__":
    csv_webeditor = App(root)
    t1 = threading.Thread(target=streaming, args=())
    t1.daemon = True
    t1.start()
    root.mainloop()
