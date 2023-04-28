from tkinter import *

win = Tk()
win.geometry("500x300")
win.overrideredirect(True)
win.attributes('-topmost', True)

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# Tính toán vị trí can giữa
x = (screen_width / 2) - (500 / 2)
y = (screen_height / 2) - (300/ 2)

# Thiết lập vị trí và kích thước cho cửa sổ
win.geometry('%dx%d+%d+%d' % (500, 300, x, y))

# title_bar = Frame(win, bg = "red", relief="raised", bd=1)
# title_bar.pack(expand=1, fill=X)

# title_laber = Label(title_bar, text="Con meo", bg = "white", fg= "black")
# title_laber.pack(side=LEFT, pady=2)

# my_button = Button(win, text= "CLOSE!", font=("Helvetica, 32"),  command= win.quit)
# my_button.pack(pady = 100)

win.mainloop()
