from collections.abc import Callable, Sequence
from tkinter import *
from threading import Thread
from tkinter import ttk
from typing import Any

from BLL.CustomerBLL import CustomerBLL
from detection.detection import Detection
from detection.record import Record
from detection.training import Training


class HomeGUI(Frame):
    def __init__(self):
        self.__home = Tk()
        self.init_components()

    def init_components(self):
        self.__home.configure(bg="#191919")
        self.__home.title("Home")
        self.__home.resizable(False, False)
        x = int((self.__home.winfo_screenwidth()/2) - (850/2))
        y = int((self.__home.winfo_screenheight()/2) - (400/2))
        self.__home.geometry('%dx%d+%d+%d' % (850, 400, x, y))
        # self.__home.attributes('-topmost', True)

        self.Homecontent = Frame(bg="#ffffff", width=850, height=400)
        self.Homecontent.master = self.__home
        self.Homecontent.pack(side="left", fill="both", expand=True)

        self.frame1 = Frame(self.Homecontent, bg="#ffffff", width=200, height=400)
        self.frame1.pack(side="left", fill='both', expand=True)

        self.frame2 = Frame(self.Homecontent, bg="#FFFFFF", width=650, height=400)
        self.frame2.pack(side="right", fill='both', expand=True)

        self.pane1 = Frame(self.frame1, bg="#7FFF00", width=200, height=50)
        self.pane1.pack(side="left", expand=True)
        self.pane1.place(x=0, y=0)

        self.pane2 = Frame(self.frame1, bg="#7FFF00", width=200, height=50)
        self.pane2.pack(side="left", expand=True)
        self.pane2.place(x=0, y=55)


        self.laber1 = Label(self.pane1, bg="#7FFF00", text="Khách hàng", font=("Times New Roman", 15, "bold"), fg="black")
        self.laber1.place(x=50, y=15)
        self.laber2 = Label(self.pane2, bg="#7FFF00", text="Thông tin", font=("Times New Roman", 15, "bold"), fg="black")
        self.laber2.place(x=50, y=15)

        self.customerBLL = CustomerBLL()

        self.frame3 = Frame(self.frame2, bg="#FFFFFF", width=600)
        self.frame3.place(x=0, y=0)

        self.panel3 = Frame(self.frame3, bg="#333333", width=260)
        self.panel3.pack(side="left", fill="y")

        self.columnNames = self.customerBLL.getCustomerDAL().getColumnNames()
        self.panel4 = Frame(self.frame3, bg="#FFFFFF", width=350)
        self.panel4.pack(side="right", fill="y")

        self.pnlCustomerConfiguration = Frame(self.panel4, bg="#FFFFFF", width=350)
        self.pnlCustomerConfiguration.pack(padx=10, pady=10)

        self.labelForm = []
        self.TextFieldsForm = []
        self.row = 0
        self.column = 0
        for i in range(0, len(self.columnNames)-1):
            self.labelForm.append(Label(self.pnlCustomerConfiguration, text=self.columnNames[i] + ": ", fg="#000000", bg="#ffffff"))
            self.labelForm[i].grid(row=self.row, column=self.column, padx=20, pady=10)
            self.column = self.column + 1
            if self.columnNames[i] == "CUSTOMER_ID":
                self.TextFieldsForm.append(Entry(self.pnlCustomerConfiguration, fg="#000000", bg="#ffffff", width=30))
                self.TextFieldsForm[len(self.TextFieldsForm)-1].insert(0, self.customerBLL.getAutoID())
                self.TextFieldsForm[len(self.TextFieldsForm)-1].configure(state='readonly')
                self.TextFieldsForm[len(self.TextFieldsForm)-1].grid(row=self.row, column=self.column, padx=20, pady=10, ipady=4)
            elif self.columnNames[i] == "GENDER":
                self.cbbGender = ttk.Combobox(self.pnlCustomerConfiguration, values=["Nam", "Nữ"], width=27)
                self.cbbGender.configure(state="readonly")
                self.cbbGender.grid(row=self.row, column=self.column, padx=20, pady=10, ipady=4)
            elif self.columnNames[i] == "MEMBERSHIP":
                self.cbbMembership = ttk.Combobox(self.pnlCustomerConfiguration, values=["Có", "Không"], width=27)
                self.cbbMembership.bind("<<ComboboxSelected>>", self.active)
                self.cbbMembership.configure(state="readonly")
                self.cbbMembership.grid(row=self.row, column=self.column, padx=20, pady=10, ipady=4)
            else:
                self.TextFieldsForm.append(Entry(self.pnlCustomerConfiguration, fg="#000000", bg="#ffffff", width=30))
                self.TextFieldsForm[len(self.TextFieldsForm)-1].grid(row=self.row, column=self.column, padx=20, pady=10, ipady=4)

            self.row = self.row + 1
            self.column = 0

        # self.laber2.place(x=10, y=10)

        self.frameimg = Frame(self.panel3, bg="black", width=200, height=310)
        self.frameimg.grid(row=0, column=1,  padx=20, pady=20, ipady=4)

        self.btRecord = Button(self.panel3, text="Đăng ký gương mặt", width=25, bg="#AFD1DF", command=self.sinupFace)
        self.btRecord.grid(row=1, column=1, ipady=4)
        self.btRecord.grid_remove
        self.panel3.grid_rowconfigure(1, minsize=0)
        self.panel3.grid_columnconfigure(1, minsize=0)

        self.detection = Detection(self.TextFieldsForm)
        self.btDetection = Button(self.panel3, text="Tìm kiếm bằng gương mặt", width=25, bg="#AFD1DF", command=self.findByFace)
        self.btDetection.grid(row=1, column=1, ipady=4)

        self.frameenter = Frame(self.pnlCustomerConfiguration, bg="#FFFFFF")
        self.frameenter.grid(row=self.row, column=1, ipady=4)

        self.btregister = Button(self.frameenter, text="Đăng nhập" ,width= 10 ,bg="#AFD1DF", command= self.actregister, state="disabled")
        self.btregister.grid(row=self.row, column=0, padx=20, pady=10, ipady=4)

        self.btlongin = Button(self.frameenter, text="Đăng ký" ,width= 10 ,bg="#AFD1DF", command= self.actlogin)
        self.btlongin.grid(row=self.row, column=1, padx=20, pady=10, ipady=4)

        self.__home.mainloop()

    def active(self, event):
        if event.widget.get() == "Có":
            self.btRecord.configure(state="normal")
        else:
            self.btRecord.configure(state="disabled")

    def sinupFace(self):
            self.record = Record(self.TextFieldsForm[0].get())
            thread = Thread(target=self.record.recording)
            thread.start()

    def findByFace(self):
        thread = Thread(target=self.detection.findByFace(self.cbbGender, self.cbbMembership))
        thread.start()

    def actregister(self):
        self.btDetection.grid()
        self.btRecord.grid_remove()
        self.panel3.grid_rowconfigure(1, minsize=0)
        self.panel3.grid_columnconfigure(1, minsize=0)

        self.btregister.configure(state="disabled")
        self.btlongin.configure(state="normal")

    def actlogin(self):
        self.btDetection.grid_remove()
        self.btRecord.grid()
        self.panel3.grid_rowconfigure(1, minsize=0)
        self.panel3.grid_columnconfigure(1, minsize=0)

        self.btregister.configure(state="normal")
        self.btlongin.configure(state="disabled")

