# import tkinter as tk

# root = tk.Tk()

# # Tạo canvas với kích thước 300x300
# canvas = tk.Canvas(root, width=300, height=300)
# canvas.pack()

# # Vẽ hình vuông với các tọa độ và kích thước
# x1, y1 = 50, 50
# x2, y2 = 250, 250
# canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

# # Chạy vòng lặp chính của ứng dụng
# root.mainloop()


# import tkinter as tk

# root = tk.Tk()

# # Tạo canvas với kích thước 300x300
# canvas = tk.Canvas(root, width=300, height=300)
# canvas.pack()

# # Vẽ hình chữ nhật và đặt label lên trên nó để tạo button
# button_rect = canvas.create_rectangle(50, 50, 150, 100, fill='blue')
# button_label = canvas.create_text(100, 75, text='Click me', fill='white')

# # Thêm sự kiện click cho button
# def button_click(event):
#     print('Button clicked!')

# canvas.tag_bind(button_rect, '<Button-1>', button_click)

# # Chạy vòng lặp chính của ứng dụng
# root.mainloop()


#import tkinter as tk

# root = tk.Tk()
# root.geometry('300x300')

# # Tạo một frame
# frame = tk.Frame(root, width=200, height=100, bg='black')
# frame.pack()


# # Thêm một label vào frame
# label = tk.Label(frame, text='This is a label')
# root.overrideredirect(True)
# label.place(x = 10, y = 10, width= 100, height= 50 )

# # Lấy kích thước của màn hình
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# # Tính toán vị trí của cửa sổ để căn giữa màn hình
# x = (screen_width - 300) // 2
# y = (screen_height - 300) // 2

# # Đặt vị trí của cửa sổ
# root.geometry('300x300+{}+{}'.format(x, y))

# # Thêm một label vào cửa sổ
# label = tk.Label(root, text='Hello, world!')
# label.pack()


# # Chạy vòng lặp chính của ứng dụng

# root.attributes('-topmost' ,True) #luôn hiển thị trên cửa sổ khác
# root.mainloop()





# import tkinter as tk
# from face_recognition.src.custom.RoundFrame import RoudFrame

# # Tạo cửa sổ
# root = tk.Tk()

# # Tạo canvas
# root.overrideredirect(True)

# # Vẽ hình chữ nhật bo góc tròn
# x1, y1, x2, y2 = 50, 50, 150, 150
# r = 20
# root.create_arc(x1, y1, x1 + r * 2, y1 + r * 2, start=90, extent=90, style='arc')
# root.create_arc(x2 - r * 2, y1, x2, y1 + r * 2, start=0, extent=90, style='arc')
# root.create_arc(x2 - r * 2, y2 - r * 2, x2, y2, start=270, extent=90, style='arc')
# root.create_arc(x1, y2 - r * 2, x1 + r * 2, y2, start=180, extent=90, style='arc')
# # Chạy vòng lặp chính của ứng dụng
# root.mainloop()

# # Create the main window
# root = tk.Tk()
# root.geometry("300x200")
# root.configure(background='white')

# # Create a rounded frame
# frame = RoudFrame(root, text="My App", corner_radius=10)
# frame.place(relx=0.5, rely=0.5, anchor="center")
# frame.pack(fill='both', expand=True)

# root.mainloop()
