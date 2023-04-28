import os
from tkinter import *
from tkinter import messagebox

import cv2
import numpy as np
from BLL.CustomerBLL import CustomerBLL
from DTO.Customer import Customer


class Detection:
    def __init__(self, textfield) -> None:
        self.customerBLL = CustomerBLL()
        self.customerID = ''
        self.textfield = textfield
        self.face_cascade = cv2.CascadeClassifier(r'face_recognition\src\detection\haarcascade_frontalface_default.xml')
        self.training_dir = r'face_recognition\classifiers'
        self.models = {}
        for filename in os.listdir(self.training_dir):
            customerID = filename.split('.')[0]
            self.models[customerID] = cv2.face.LBPHFaceRecognizer_create()
            self.models[customerID].read(os.path.join(self.training_dir, filename))

    def detect(self):
        cap = cv2.VideoCapture(0)

        while (True):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                self.customerID = ''
                minimum = 100
                confidences = []
                for model_id, model in self.models.items():
                    label, confidence = model.predict(roi_gray)
                    confidences.append(confidence)
                    if confidence < 50 and confidence < minimum:
                        self.customerID = model_id

                if self.customerID != '':
                    self.customer = self.customerBLL.findCustomersBy({"CUSTOMER_ID": self.customerID})[0]
                    print(self.customer)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, self.customerID, (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)

                    self.textfield[1].delete(0, END)
                    self.textfield[1].insert(END, self.customer.getCustomerID())
                    # name.configure(state="normal")
                    # name.delete(0, END)
                    # name.insert(END, self.customer.getName())
                    # name.configure(state="disabled")
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                if self.customerID == '':
                    print ("Không nhận diện được khuôn mặt.")
                    self.textfield[1].delete(0, END)
                    # name.configure(state="normal")
                    # name.delete(0, END)
                    # name.configure(state="disabled")
                    if messagebox.askyesno("Thông báo", "Không nhận diện được khách hàng.\nTạo khách hàng mới?"):
                        self.customer = Customer(customerID=self.customerBLL.getAutoID())
                        self.customerBLL.addCustomer(self.customer)
                        self.textfield[1].insert(END, self.customer.getCustomerID())
                        # name.configure(state="normal")
                        # name.insert(END, self.customer.getName())
                        # name.configure(state="disabled")
                break
        cap.release()
        cv2.destroyAllWindows()
        self.customerID = ''

    def findByFace(self, cbbGender, cbbMembership):
        cap = cv2.VideoCapture(0)

        while (True):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                self.customerID = ''
                minimum = 100
                confidences = []
                for model_id, model in self.models.items():
                    label, confidence = model.predict(roi_gray)
                    confidences.append(confidence)
                    if confidence < 50 and confidence < minimum:
                        self.customerID = model_id

                if self.customerID != '':
                    self.customer = self.customerBLL.findCustomersBy({"CUSTOMER_ID": self.customerID})[0]
                    values = self.customer.__str__().split(" | ")
                    print(self.customer)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, self.customerID, (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)
                    self.textfield[0].configure(state="normal")
                    self.textfield[0].delete(0, END)
                    self.textfield[0].insert(END, values[0])
                    self.textfield[0].configure(state="readonly")

                    self.textfield[1].delete(0, END)
                    self.textfield[1].insert(END, values[1])

                    cbbGender.configure(state="normal")
                    cbbGender.set(values[2])
                    cbbGender.configure(state="readonly")

                    self.textfield[2].delete(0, END)
                    self.textfield[2].insert(END, values[3])

                    self.textfield[3].delete(0, END)
                    self.textfield[3].insert(END, values[4])

                    cbbMembership.configure(state="normal")
                    cbbMembership.set(values[5])
                    cbbMembership.configure(state="readonly")

                    self.textfield[4].delete(0, END)
                    self.textfield[4].insert(END, values[6])

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                if self.customerID == '':
                    print ("Không nhận diện được khuôn mặt.")

                    messagebox.showinfo("Thông báo", "Không nhận diện được khách hàng")
                break
        cap.release()
        cv2.destroyAllWindows()
        self.customerID = ''
