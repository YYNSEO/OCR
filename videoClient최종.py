
import socket
import cv2  # OpenCV
import tkinter  # Tkinter 및 GUI 관련
import tkinter as tk
import PIL.Image, PIL.ImageTk
import numpy as np
import threading  # Thread
from queue import Queue

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')     # 학습된 데이터 불러옴

root = tk.Tk()
result_img = 0  # 전역변수로 최종 이미지를 받도록 했다
click_pos=(320,240)
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
        self.canvas = tkinter.Canvas(self.master, width=608, height=480)
        self.canvas.pack()
        self.label = tkinter.Label(self.master, width=20, height=5)
        self.label.pack()
        self.btn = tkinter.Button(self.label,text="흑백 + 블러필터",width=20, height=5, command=self.change)
        self.btn.pack(side="left")
        self.btn2 = tkinter.Button(self.label,text="2m 필터",width=20, height=5, command=self.flagschange)
        self.btn2.pack(side="left")
        self.btn3 = tkinter.Button(self.label,text="원본",width=20, height=5, command=self.flagchange)
        self.btn3.pack(side="left")
        self.btn4 = tkinter.Button(self.label,text="정재현",width=20, height=5, command=self.flagchange_jjh)
        self.btn4.pack(side='left')
        self.btn5 = tkinter.Button(self.label, text="김영기", width=20, height=5, command=self.flagchange_kyg)
        self.btn5.pack(side='left')
        self.btn6 = tkinter.Button(self.label, text="윤하얀", width=20, height=5, command=self.flagchange_yhy)
        self.btn6.pack(side='left')
        self.btn7 = tkinter.Button(self.label, text="김지욱", width=20, height=5, command=self.flagchange_kju)
        self.btn7.pack(side='left')
        self.btn8 = tkinter.Button(self.label, text="진정현", width=20, height=5, command=self.flagchange_jinjeonghyun)
        self.btn8.pack(side='left')
        self.btn9 = tkinter.Button(self.label, text="김자연", width=20, height=5, command=self.flagchage_knature)
        self.btn9.pack(side='left')
        self.update()
        self.wavefilter_count = 0
        self.e = cv2.VideoCapture("e.mp4")
        self.img_tree = cv2.imread('tree1.png', cv2.IMREAD_COLOR)
        self.img_tree = cv2.resize(self.img_tree, (263, 186))
        self.img_tree = cv2.cvtColor(self.img_tree, cv2.COLOR_BGR2RGB)

    def flagchage_knature(self):
        self.flags=8
    def flagchange_kju(self):
        self.flags=6#김지욱
    def flagchange_jjh(self):
        self.flags = 3#정재현
    def flagchange_yhy(self):
        self.flags = 5#윤하얀
    def flagchange_jinjeonghyun(self):
        self.flags=7#진정현
    def flagchange_kyg(self):
        self.flags = 4  #김영기
    def flagschange(self):
        self.flags=2
    def flagchange(self):
        self.flags=0
    def change(self):
        self.flags = 1
    def update(self):
        try:
            vid = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            #->필터함수호출
            #필터에서 리턴받은 결과 프레임
            if self.flags == 1:
                vid = self.filter(vid)
            if self.flags==2:
                vid=self.add(vid)
            if self.flags==3:
                vid=self.filter_jjh(vid)#정재현
            if self.flags == 4:
                vid = self.filter_kyg(vid)  # 김영기
            if self.flags == 5:
                vid = self.filter_yhy(vid)  # 김영기
            if self.flags==6:
                vid=self.filter_kyu(vid)#김지욱
            if self.flags==7:
                vid=self.filter_jinjeonghyun(vid)#진정현
            if self.flags==8:
                vid=self.filter_knature(vid)#김자연
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(vid))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        except:
            pass
        self.master.after(self.delay, self.update)
    def add(self, frame):
        height, width = frame.shape[:2]
        scale_factor = 2
        new_height = int(height * scale_factor)
        delta = int((new_height - height) / 2)
        stretched_frame = cv2.resize(frame, (width, new_height))
        if delta > 0:
            stretched_frame = stretched_frame[delta:-delta, :]
        return stretched_frame
    def filter(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blr = cv2.GaussianBlur(gray, (0, 0), 2)
        return blr

    def dual_filter(self,frame):
        #height, width = frame.shape[:2]
        print(frame.shape)
        #if frame.shape[1] % 2 != 0:
        frame = frame[:-240, :-320]
        frame_left = frame.copy()
        #frame_right = frame.copy()


        combined_frame=cv2.hconcat([frame,frame_left])
        combined_frame2=combined_frame.copy()
        res=cv2.vconcat([combined_frame,combined_frame2])

        #combined_frame=cv2.resize(frame_right,(width/2,height/2))

        #frame_rgb = cv2.cvtColor(combined_frame, cv2.COLOR_BGR2RGB)
        #img = PIL.Image.fromarray(combined_frame)
        return res
    def filter_jjh(self,frame):
        global click_pos
        click_x, click_y = click_pos
        # 웹캠화면에 안찍히는 부분은 확대못하니까 예외처리
        if 64 < click_x < 576 and 48 < click_y < 432:
            #decimg = cv2.imdecode(frame, 1)  # 이미지디코딩
            #ad = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
            result_image = cv2.resize(frame, (640, 480))
            original_frame = result_image.copy()

            # 일정비율로 커지는 돋보기로 쓸 화면만들기
            res9 = original_frame[click_y - 24:click_y + 24, click_x - 32:click_x + 32]
            res8 = original_frame[click_y - 21:click_y + 21, click_x - 28:click_x + 28]
            res7 = original_frame[click_y - 18:click_y + 18, click_x - 24:click_x + 24]
            res6 = original_frame[click_y - 15:click_y + 15, click_x - 20:click_x + 20]
            res5 = original_frame[click_y - 12:click_y + 12, click_x - 16:click_x + 16]
            res4 = original_frame[click_y - 9:click_y + 9, click_x - 12:click_x + 12]

            for i, res in enumerate([res9, res8, res7, res6, res5, res4], start=1):
                height, width = res.shape[:2]
                resized_width, resized_height = width * 2, height * 2  # 확대시키기

                start_x = click_x - resized_width // 2
                start_y = click_y - resized_height // 2

                # 확대시킨 너비와 높이 넣어서 리사이즈하기 보간법:interpolation=cv2.INTER_LINEAR
                res_resized = cv2.resize(res, (resized_width, resized_height), interpolation=cv2.INTER_LINEAR)
                if i == 6:  # 가장안쪽영역은 필터없이
                    pass
                    res_blurred = res_resized
                else:  # 나머진 바깥쪽이 가장 필터약하고 안으로 들어갈수록 필터세게
                    gaussian_size = 5 + 2 * (i - 1)  # 커널값
                    sigma = i * 2 - 1
                    res_blurred = cv2.GaussianBlur(res_resized, (gaussian_size, gaussian_size), sigma)

                # 리사이즈와 필터를 입힌 화면을 원본화면에 씌우기
                result_image[start_y:start_y + resized_height, start_x:start_x + resized_width] = res_blurred

        return result_image
    def filter_kyg(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 2)  # 불러온 데이터 기반으로 객체 검출
        # minNeighbors : n개의 사각형이 중복되어야 검출
        # scaleFactor : 화면 확대 비율
        for (x, y, w, h) in faces:  # x, y : 시작 위치(좌상단)
            # print(x, y, w, h)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 모자이크 처리할 영역 추출
            roi = frame[y:y + h, x:x + w]  # 얼굴 영역
            # 추출한 영역 축소 후 확대 (모자이크 효과)
            factor = 10  # 모자이크 픽셀 크기 조절
            small_roi = cv2.resize(roi, (w // factor, h // factor))
            mosaic_roi = cv2.resize(small_roi, (w, h), interpolation=cv2.INTER_NEAREST)
            # 모자이크 처리된 영역을 원본 이미지에 적용
            frame[y:y + h, x:x + w] = mosaic_roi
        return frame
    def filter_yhy(self,frame):
            if frame is not None:
                rows, cols = frame.shape[:2]  # 너비 추출
                exp = 0.6  # 오목 지수
                scale = 1.3  # 변환 영역 크기
                map_y, map_x = np.indices((rows, cols), dtype=np.float32)  # x좌표와 y좌표를 담고 있는 매핑 배열 생성
                # 좌상단 기준좌표에서 -1~1로 정규화된 중심점 기준 좌표로 변경
                # 이미지 픽셀 좌표를 일반화하여 [-1,1] 범위로 정규화하는 연산
                map_x = 2 * map_x / (cols - 1) - 1
                map_y = 2 * map_y / (rows - 1) - 1
                # 직교좌표를 극 좌표로 변환 / r: 각 픽셀의 중심으로부터의 거리 , theta: 각 픽셀의 중심에서 x축까지의 각도를 나타내는 배열
                r, theta = cv2.cartToPolar(map_x, map_y)
                # 왜곡 영역만 중심 축소 지수 적용
                # 거리(r)가 특정 값(scale)보다 작은 픽셀들의 거리(r)를 제곱하는 연산을 수행
                r[r < scale] = r[r < scale] ** exp  # r[r < scale]는 r 배열에서 scale보다 작은 값을 가지는 요소들로 이루어진 배열을 선택
                # 이후에 선택된 요소들에 대해서는 제곱 연산을 수행하여 거리를 변형시킴
                # 결과적으로 r 배열에서 scale보다 작은 값들의 거리를 제곱하여 강조하는 효과를 얻게 된다.
                # 극 좌표를 직교좌표로 변환
                map_x, map_y = cv2.polarToCart(r, theta)
                # 중심점 기준에서 좌상단 기준으로 변경
                map_x = ((map_x + 1) * cols - 1) / 2
                map_y = ((map_y + 1) * rows - 1) / 2
                # 재매핑 변환
                distorted = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)
                return distorted
    def filter_kyu(self,decimg):
                tree_area = decimg[:self.img_tree.shape[0], :self.img_tree.shape[1]]
                result = cv2.add(tree_area, self.img_tree)
                decimg[:self.img_tree.shape[0], :self.img_tree.shape[1]] = result
                if self.e.get(cv2.CAP_PROP_POS_FRAMES) == self.e.get(cv2.CAP_PROP_FRAME_COUNT):
                    self.e.set(cv2.CAP_PROP_POS_FRAMES, 0)
                rt1, frame1 = self.e.read()
                frame1 = cv2.resize(frame1, (decimg.shape[1], decimg.shape[0]))
                decimg = cv2.add(decimg, frame1)
                return decimg
    def filter_knature(self,frame):
            rows, cols = frame.shape[:2]  # 형태(shape) 속성에서 첫 번째와 두 번째 차원의 크기를 가져오는 것
            mapy, mapx = np.indices((rows, cols), dtype=np.float32)  # 이미지의 각 픽셀에 대한 행과 열의 인덱스를 생성
            mapx = mapx.astype(np.float32)  # 인덱스 배열을 부동소수점 형식으로 변환
            mapy = mapy.astype(np.float32)
            self.wavefilter_count += 1  # wavefilter 호출 횟수 증가
            # if self.w_count < -3 or self.w_count > 3:
            #     self.w_direction *= -1  # 방향을 바꾸어주기 위해 -1을 곱함
            #
            # self.w_count += self.w_direction
            displacement = self.wavefilter_count * 30  # 축 방향으로 이동할 거리를 설정
            mapy_shifted = mapy + displacement  # 축 방향으로 이동시킨 mapy 변수 생성
            l = 60  # 주기는 고정
            amp = 50
            sinx = mapx + amp * np.sin(mapy_shifted / l)  # sin 함수에 이동된 mapy 변수 적용
            # sinx = mapx + amp * np.sin(self.w_direction*mapy / l)
            cosy = mapy + amp * np.cos(mapx / l)
            img_sinx = cv2.remap(frame, sinx, mapy, cv2.INTER_LINEAR)

            return img_sinx
    def filter_jinjeonghyun(self,decimg2):
        elephant = cv2.imread('elephant.png', cv2.IMREAD_COLOR)
        while True:



                reflect1 = np.fliplr(decimg2)
                width_half = reflect1.shape[1] // 2
                left_half = reflect1[:, :width_half]
                reflect1[:, width_half:] = np.fliplr(left_half)

                reflect2 = np.flip(decimg2, (0, 1))
                width_half2 = reflect2.shape[1] // 2
                left_half2 = reflect2[:, :width_half2]
                reflect2[:, width_half2:] = np.fliplr(left_half2)

                decimg2[: reflect2.shape[0] // 2, :] = reflect1[: reflect2.shape[0] // 2, :]
                decimg2[reflect2.shape[0] // 2:, :] = reflect2[reflect2.shape[0] // 2:, :]

                mask = np.full_like(elephant, 255)
                center = (320, 240)
                final_img = cv2.seamlessClone(elephant, decimg2, mask, center, cv2.MIXED_CLONE)
                return final_img

if __name__ == "__main__":
    csv_webeditor = App(root)
    t1 = threading.Thread(target=streaming, args=())
    t1.daemon = True
    t1.start()
    root.mainloop()