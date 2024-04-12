import os
from threading import Thread
from time import sleep
from tkinter import messagebox
from PIL import Image, ImageTk

import cv2
from detection.training import Training


class Record:
    def __init__(self, customerID) -> None:
        self.customerID = customerID
        self.roi_gray = None
        self.flag = False
        self.face_dir = "face_recognition/faces"
        try:
            os.mkdir(self.face_dir)
        except:
            pass

    def show_instruction(self):
        pass

    def take_pictures(self):
        new_dir = fr'{self.face_dir}\{self.customerID}'
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        self.i = 0
        while self.i < 40:
            sleep(1)
            if self.roi_gray is not None:
                cv2.imwrite(fr"{new_dir}\{self.i:03}.jpg", self.roi_gray)
            else:
                self.i -= 1
            self.i += 1
        self.flag = True


    def recording(self):
        face_cascade = cv2.CascadeClassifier(r'face_recognition\src\detection\haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        thread = Thread(target=self.take_pictures)
        thread.start()
        while (True):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                self.roi_gray = gray[y:y+h, x:x+w]

                pos = (x + 10, y + h - 10)
                if self.i < 10:
                    cv2.putText(frame, "Nhin len", pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)
                elif self.i < 20:
                    cv2.putText(frame, "Nhin xuong", pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)
                elif self.i < 30:
                    cv2.putText(frame, "Nhin trai", pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)
                else:
                    cv2.putText(frame, "Nhin phai", pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)

            if self.flag:
                messagebox.showinfo("Message", "Đăng ký thành công!")
                self.flag = False
                break
            cv2.imshow('Sign up', frame)
            if cv2.waitKey(1) == ord('a'):
                break
        cap.release()
        cv2.destroyAllWindows()

        Training().train(self.customerID)

    def take_camera(self):
        new_dir = fr'face_recognition\imgid\{self.customerID}'
        if self.roi_gray is not None:
            cv2.imwrite(fr"{new_dir}.png", self.roi_gray)
            self.flag = True


    def imgcamrera(self, label1):
        face_cascade = cv2.CascadeClassifier(r'face_recognition\src\detection\haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        while (True):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                self.roi_gray = frame[y:y+h, x:x+w]

                # pos = (x + 10, y + h - 10)
                cv2.putText(frame, "Nhin thang", (x, y+h+25),  cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                if len(faces) == 0:
                    continue
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2)
                self.flag = True
                break

        self.take_camera()
        if self.flag:
            self.imgMode = ImageTk.PhotoImage(Image.open(fr'face_recognition\imgid\{self.customerID}.png').resize((180, 150), Image.ANTIALIAS))
            label1.configure(image=self.imgMode, anchor="center", width=180, height= 150)
            messagebox.showinfo("Message", "Chup anh khuon mat thanh cong.")
            self.flag = False
        cap.release()
        cv2.destroyAllWindows()


