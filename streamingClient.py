import tkinter as tk
from tkinter import filedialog
import pandas as pd
from io import StringIO
import PIL.Image, PIL.ImageTk
import cv2
import threading
result_img = 0

class Streaming:
    def __init__(self, master):
        self.master=master
        self.master.geometry("1200x800")
        self.master.title("스트리밍")
        self.delay = 15
        self.webcam = tk.Canvas(self.master, width=800, height=400,background="white")
        self.webcam.pack()
        self.update()
        self.master.mainloop()

        self.one = tk.Button(self.master, text="원본")
        self.one.pack(side='left')
        self.two = tk.Button(self.master, text="블러처리")
        self.two.pack(side='left')
        self.three = tk.Button(self.master, text="늘리기")
        self.three.pack(side='left')

    def update(self):
        try:
            vid = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(vid))
            self.webcam.create_image(0, 0, image=self.photo, anchor=tk.NW)
        except:
            pass
        self.master.after(self.delay, self.update)


    def load_csv(self):
        file_path=filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        #filedialog.askopenfilename()
        #filedialog에서 제공하는 파일 대화상자를 통한 파일 선택 메서드
        if file_path:
            try:
                self.df = pd.read_csv(file_path, encoding='cp949') # 인코딩방식 1
                print(type(self.df))
            except:
                self.df = pd.read_csv(file_path, encoding='utf-8') # 인코딩 방식 1
            #cp949인코딩에서 오류나면 utf-8로 열도록 에외처리
            self.text_box.delete(0.0,tk.END)
            self.text_box.insert(tk.END, self.df.to_string(index=False))
            # df는 데이터프레임이라는 판다스에서 제공하는 데이터 형태이고 엑셀, csv같은 테이블 구조
            # 데이터 프레임은 0부터 인덱스를 가진다.
            # to_string메서드는 데이터프레임을 문자열로 반환

    def save_change(self):
        if hasattr(self, 'df'): # hasattr 속성을 가지고 있냐를 체크하는 함수
            edited_data = self.text_box.get('0.0', tk.END)
            edited_df = pd.read_csv(StringIO(edited_data))
            file_path = filedialog.askopenfilename(defaultextension='.csv',filetypes=[("CSV Files", "*.csv")])
            if file_path:
                edited_df.to_csv(file_path,index=False)
                tk.messagebox.showinfo("success", "변경 완료")

root = tk.Tk()
csv_editor=Streaming(root)
csv_editor.master.mainloop()