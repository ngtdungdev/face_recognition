from collections.abc import Callable, Sequence
from datetime import datetime
from tkinter import *
from threading import Thread
from tkinter import ttk
from typing import Any
from PIL import Image, ImageTk

from BLL.CustomerBLL import CustomerBLL
from DTO.Customer import Customer
from detection.detection import Detection
from detection.record import Record
from detection.training import Training


class HomeGUI(Frame):
    def __init__(self):
        self.__home = Tk()
        self.init_components()

    def init_components(self):
        self.record = None
        self.__home.configure(bg="#191919")
        self.__home.title("Home")
        self.__home.resizable(False, False)
        x = int((self.__home.winfo_screenwidth()/2) - (850/2))
        y = int((self.__home.winfo_screenheight()/2) - (450/2))
        self.__home.geometry('%dx%d+%d+%d' % (850, 450, x, y))
        # self.__home.attributes('-topmost', True)

        self.Homecontent = Frame(bg="#ffffff", width=850, height=450)
        self.Homecontent.master = self.__home
        self.Homecontent.pack(side="left", fill="both", expand=True)

        self.frame1 = Frame(self.Homecontent, bg="#ffffff", width=200, height=450)
        self.frame1.pack(side="left", fill='both')

        self.frame2 = Frame(self.Homecontent, bg="#ffffff", width=670, height=450)
        self.frame2.pack(side="right", fill='both', expand=True)

        self.pane1 = Frame(self.frame1, bg="#D3D3D3", width=200, height=50)
        self.pane1.pack(side="left", expand=True)
        self.pane1.place(x=0, y=0)

        self.pane2 = Frame(self.frame1, bg="#7FFF00", width=200, height=50)
        self.pane2.pack(side="left", expand=True)
        self.pane2.place(x=0, y=55)

        self.laber1 = Label(self.pane1, bg="#D3D3D3", text="Khách hàng", font=("Times New Roman", 15, "bold"), fg="black")
        self.laber1.bind('<Button-1>', self.labelclient)
        self.laber1.place(x=50, y=15)

        self.laber2 = Label(self.pane2, bg="#7FFF00", text="Thông tin", font=("Times New Roman", 15, "bold"), fg="black")
        self.laber2.bind('<Button-1>', self.labelinfor)
        self.laber2.place(x=50, y=15)

        self.labelclient(None)

        self.__home.mainloop()

    def active(self, event):
        if event.widget.get() == "Có":
            self.btRecord.configure(state="normal")
        else:
            self.btRecord.configure(state="disabled")

    def sinupFace(self):
        thread = Thread(target=self.record.recording)
        thread.start()

    def camera(self):
        thread = Thread(target=self.record.imgcamrera(self.label1))
        thread.start()

    def findByFace(self):
        self.detection = Detection(self.TextFieldsForm)
        thread = Thread(target=self.detection.findByFace(self.cbbGender, self.cbbMembership, self.btdelete, self.label1))
        thread.start()

    def actedit(self):
        self.btDetection.grid()
        self.btRecord.grid_remove()
        self.panel3.grid_rowconfigure(1, minsize=0)
        self.panel3.grid_columnconfigure(1, minsize=0)
        self.TextFieldsForm[0].configure(state="normal")
        self.TextFieldsForm[0].delete(0, END)
        self.TextFieldsForm[0].insert(END, "")

        self.btcreate.configure(state="normal")
        self.btres.configure(state="normal")
        self.btres.configure(state="disabled")
        self.btedit.configure(state="disabled")
        self.label1.destroy()
        self.label1 = Label(self.img, image=None, width=25, height= 10)
        self.label1.pack(fill=BOTH, expand=TRUE)
        self.label1.grid(row=0, column=1, padx=40, pady=25, sticky="nsew")

    def actcreate(self):
        self.btDetection.grid_remove()
        self.btRecord.grid()
        self.panel3.grid_rowconfigure(1, minsize=0)
        self.panel3.grid_columnconfigure(1, minsize=0)
        self.TextFieldsForm[0].insert(0, self.customerBLL.getAutoID())
        self.TextFieldsForm[0].configure(state="disabled")

        self.btcreate.configure(state="disabled")
        self.btres.configure(state="normal")
        self.btedit.configure(state="normal")
        self.btdelete.configure(state="disabled")
        self.record = Record(self.TextFieldsForm[0].get())


    def actcancel(self):
        for i in range(0, len(self.TextFieldsForm)):
            self.TextFieldsForm[i].delete(0, END)
            self.TextFieldsForm[i].insert(END, "")
        self.cbbGender.configure(state="normal")
        self.cbbGender.delete(0, END)
        self.cbbGender.configure(state="readonly")
        self.cbbMembership.configure(state="normal")
        self.cbbMembership.delete(0, END)
        self.cbbMembership.configure(state="readonly")
        self.TextFieldsForm[0].configure(state="normal")
        self.TextFieldsForm[0].delete(0, END)
        self.TextFieldsForm[0].insert(END, "")
        self.label1.destroy()
        self.label1 = Label(self.img, image=None, width=25, height= 10)
        self.label1.pack(fill=BOTH, expand=TRUE)
        self.label1.grid(row=0, column=1, padx=40, pady=25, sticky="nsew")




    def actupdate(self):
        if (self.btedit.cget("state") != "disabled"):
            self.add()
        else:
            self.upd()

    def actdelete(self):
        print( self.TextFieldsForm[0].get())
        self.customerBLL.deleteCustomer(Customer(customerID = self.TextFieldsForm[0].get()))
        self.actcancel()

    def add(self):
        gender = True if self.cbbGender.get() == "Nam" else False
        member = True if self.cbbMembership.get() == "Có" else False
        dob = datetime.strptime(self.TextFieldsForm[2].get(), "%Y-%m-%d").date()
        dos = datetime.strptime(self.TextFieldsForm[4].get(), "%Y-%m-%d").date()
        self.newCustomer = Customer(self.TextFieldsForm[0].get(), self.TextFieldsForm[1].get(), gender, dob, self.TextFieldsForm[3].get(), member, dos, False)
        self.customerBLL.addCustomer(self.newCustomer)
        self.actcancel()

    def upd(self):
        gender = True if self.cbbGender.get() == "Nam" else False
        member = True if self.cbbMembership.get() == "Có" else False
        dob = datetime.strptime(self.TextFieldsForm[2].get(), "%Y-%m-%d").date()
        dos = datetime.strptime(self.TextFieldsForm[4].get(), "%Y-%m-%d").date()
        self.newCustomer = Customer(self.TextFieldsForm[0].get(), self.TextFieldsForm[1].get(), gender, dob, self.TextFieldsForm[3].get(), member, dos, False)
        self.customerBLL.updateCustomer(self.newCustomer)
        self.actcancel()

    def labelclient(self, even):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.customerBLL = CustomerBLL()
        self.laber1.configure(bg="#D3D3D3")
        self.laber2.configure(bg="#7FFF00")
        self.pane1.configure(bg="#D3D3D3")
        self.pane2.configure(bg="#7FFF00")
        # self.frame2 = Frame(self.Homecontent, bg="#FFFFFF", width=650, height=450)
        # self.frame2.pack(side="right", fill='both', expand=True)

        self.frame3 = Frame(self.frame2, bg="#FFFFFF", width=670, height=450)
        self.frame3.pack(padx=0, pady=0, expand=True)
        self.frame3.pack_propagate(False)


        self.panel3 = Frame(self.frame3, bg="#333333", width=300, height= 500)
        self.panel3.pack(side="left", fill="x", expand=True)

        self.columnNames = self.customerBLL.getCustomerDAL().getColumnNames()
        self.panel4 = Frame(self.frame3, bg="#FFFFFF", width=370)
        self.panel4.pack(side="right",  fill="x", expand=True)

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
                self.TextFieldsForm[len(self.TextFieldsForm)-1].configure(state="normal")
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

        self.frameimg = Frame(self.panel3, bg="#333333")
        self.frameimg.grid(row=0, column=1,sticky="nsew")

        self.img = Frame(self.frameimg, bg="#333333")
        self.img.grid(row=0, column=1, padx = 0, pady = 70, sticky="nsew")


        self.label1 = Label(self.img, width=25, height= 10)
        # # self.label1.pack_propagate(TRUE)
        self.label1.pack(fill=BOTH, expand=TRUE)
        # self.label1.grid(padx = 0, pady = 20, sticky="nsew")
        self.label1.grid(row=0, column=1, padx=40, pady=25, sticky="nsew")

        self.btres = Button(self.panel3, text="Chụp ảnh", width=25, bg="#AFD1DF", command=self.camera, state="disabled")
        self.btres.grid(row=1, column=1, padx = 40, pady = 10, ipady=4)


        self.btRecord = Button(self.panel3, text="Đăng ký gương mặt", width=25, bg="#AFD1DF", command=self.sinupFace)
        self.btRecord.grid(row=2, column=1, padx = 40, pady = 10, ipady=4)
        self.btRecord.grid_remove
        self.panel3.grid_rowconfigure(1, minsize=0)
        self.panel3.grid_columnconfigure(1, minsize=0)

        self.btDetection = Button(self.panel3, text="Tìm kiếm bằng khuôn mặt", width=25, bg="#AFD1DF", command=self.findByFace)
        self.btDetection.grid(row=2, column=1, padx = 40, pady = 10, ipady=4)

        self.frameenter = Frame(self.pnlCustomerConfiguration, bg="#FFFFFF")
        self.frameenter.grid(row=self.row, column=1, ipady=4)

        self.btupdate = Button(self.pnlCustomerConfiguration, text="Cập nhật" ,width= 10 ,bg="#AFD1DF", command=self.actupdate)
        self.btupdate.grid(row=self.row, column=0, padx=20, pady=10, ipady=4)

        self.btcreate = Button(self.frameenter, text="Tạo mới" ,width= 10 ,bg="#AFD1DF", command=self.actcreate)
        self.btcreate.grid(row=self.row, column=0, padx=20, pady=10, ipady=4)

        self.btedit = Button(self.frameenter, text="Tìm kiếm" ,width= 10 ,bg="#AFD1DF", command= self.actedit , state="disabled")
        self.btedit.grid(row=self.row, column=1, padx=20, pady=10, ipady=4)

        self.btdelete = Button(self.frameenter, text="Xóa" ,width= 10 ,bg="#AFD1DF", command= self.actdelete , state="disabled")
        self.btdelete.grid(row=self.row + 1, column=0, padx=20, pady=10, ipady=4)

        self.btcancel = Button(self.frameenter, text="Hủy" ,width= 10 ,bg="#AFD1DF", command=self.actcancel)
        self.btcancel.grid(row=self.row + 1, column=1, padx=20, pady=10, ipady=4)

    def labelinfor(self, even):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.laber1.configure(bg="#7FFF00")
        self.laber2.configure(bg="#D3D3D3")
        self.pane1.configure(bg="#7FFF00")
        self.pane2.configure(bg="#D3D3D3")

        self.tableFrame = Frame(self.frame2, width=670, height=450, bg="#333333", highlightthickness=0, borderwidth=0)
        self.tableFrame.pack(padx=0, pady=0)
        self.tableFrame.pack_propagate(False)

        self.table = ttk.Treeview(self.tableFrame, columns=self.columnNames[0:len(self.columnNames)-1], show="headings")
        self.table.heading("0", text="CUSTOMER_ID")
        self.table.column("0", width=100)
        self.table.heading("1", text="NAME")
        self.table.column("1", width=150)
        self.table.heading("2", text="GENDER")
        self.table.column("2", width=60)
        self.table.heading("3", text="DOB")
        self.table.column("3", width=80)
        self.table.heading("4", text="PHONE")
        self.table.column("4", width=80)
        self.table.heading("5", text="MEMBERSHIP")
        self.table.column("5", width=100)
        self.table.heading("6", text="DOSUP")
        self.table.column("6", width=80)
        self.data = self.customerBLL.getData()
        for row in self.data:
            self.table.insert('', END, values = row)
        self.table.pack(fill=BOTH, expand=True)

        # self.table.grid_rowconfigure(0, width=50)
        # self.table.grid_columnconfigure(0, width=50)
        # self.table.grid(row=0, column=0, width=50)

        # self.scrollbar = ttk.Scrollbar(self.tableFrame, orient="horizontal", command=self.table.xview)
        # self.table.configure(xscrollcommand=self.scrollbar.set)
        # self.scrollbar.pack(side="bottom", fill="x")

