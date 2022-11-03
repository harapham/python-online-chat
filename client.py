import socket
import threading
import json
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText


IP = ''
PORT = ''
user = ''
# user list box
listbox1 = ''
# đánh dấu xem user list có cần thay đổi không
ii = 0
# user list
users = []
chat = '------GROUP CHAT-------'
# cửa sổ đăng nhập
root1 = tkinter.Tk()
root1.title('Log in')
root1['height'] = 170
root1['width'] = 300
root1.resizable(0, 0)

# ip và port
IP1 = tkinter.StringVar()
IP1.set('127.0.0.1:50007')
User = tkinter.StringVar()
User.set('')

# server label
labeYC = tkinter.Label(root1,text='Vui lòng nhập username!',font=('Arial',10,'italic'))
labeYC.place(x=35,y=8,width=250,height=30)

labelIP = tkinter.Label(root1, text='Server address',font=('Barlow Condensed Medium',12))
labelIP.place(x=35, y=40, width=100, height=20)

entryIP = tkinter.Entry(root1, width=80, textvariable=IP1)
entryIP.place(x=140, y=40, width=130, height=30)

# username label
labelUser = tkinter.Label(root1, text='Username',font=('Barlow Condensed Medium',12))
labelUser.place(x=22, y=80, width=100, height=20)

entryUser = tkinter.Entry(root1, width=80, textvariable=User)
entryUser.place(x=140, y=80, width=130, height=30)


# login button
def login(*args):
    global IP, PORT, user
    # lấy ip và port
    IP, PORT = entryIP.get().split(':')
    PORT = int(PORT)
    user = entryUser.get()
    # kiểm tra xem user đã được nhập hay chưa, nếu chưa báo lỗi
    if not user:
        tkinter.messagebox.showerror(
            'Name type error', message='Username Empty!')
    else:
        root1.destroy()


# tạo chức năng đăng nhập trong button log in
root1.bind('<Return>', login)   ## bấm button bằng nhấn enter
but = tkinter.Button(root1, text='Log in',font=('Barlow Condensed Medium',12,'bold'), command=login)
but.place(x=110, y=120, width=90, height=40)

root1.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT)) #kết nối với server
if user=='/noname':
    # user name chế độ ẩn danh
    s.send('no'.encode())
else:
    # gửi user name
    s.send(user.encode())

# nếu không có username thì đặt username là 'ip:port'
addr = s.getsockname()  # lấy ip và username
#addr = addr[0] + ':' + str(addr[1])
if user == '/noname':
    user = 'no name'+'('+str(addr[1])+')'

# Chat room GUI
root = tkinter.Tk()
root.title(user)  # đặt tên chat room là username
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)

# tạo hộp văn bản cuộn
listbox = ScrolledText(root)
listbox.place(x=5, y=0, width=570, height=320)
# màu phông chữ của hộp văn bản
listbox.tag_config('red', foreground='#FF0000')
listbox.tag_config('blue', foreground='#2365a6')
listbox.tag_config('green', foreground='#007500')
listbox.tag_config('black', foreground='#000000')
listbox.insert(tkinter.END, 'Welcome to the chat room!','#000000')

# Emoji
# giả sử trước có 4 emoji
b1 = ''
b2 = ''
b3 = ''
b4 = ''
b5 = ''
b6 = ''
b7 = ''
b8 = ''
b9 = ''
b0 = ''
# emoji (size : 36x36)
emoji_1 = tkinter.PhotoImage(file='./emoji/1.png')
emoji_2 = tkinter.PhotoImage(file='./emoji/2.png')
emoji_3 = tkinter.PhotoImage(file='./emoji/3.png')
emoji_4 = tkinter.PhotoImage(file='./emoji/4.png')
emoji_5 = tkinter.PhotoImage(file='./emoji/5.png')
emoji_6 = tkinter.PhotoImage(file='./emoji/6.png')
emoji_7 = tkinter.PhotoImage(file='./emoji/7.png')
emoji_8 = tkinter.PhotoImage(file='./emoji/8.png')
emoji_9 = tkinter.PhotoImage(file='./emoji/9.png')
emoji_0 = tkinter.PhotoImage(file='./emoji/0.png')
# tạo dict emoji
dict = {'e1': emoji_1, 'e2': emoji_2, 'e3': emoji_3, 'e4': emoji_4, 'e5': emoji_5, 'e6': emoji_6, 'e7': emoji_7, 'e8': emoji_8, 'e9': emoji_9, 'e0': emoji_0}
ee = 0  #  đánh dấu xem ô emoji có được mở hay không


# hàm xử lý : Sau khi nhấp vào emoji, emoji sẽ được gửi
# exp là 1 emoji
def mark(exp):
    global ee
    mes = exp + ':;' + user + ':;' + chat
    s.send(mes.encode())
    b1.destroy()
    b2.destroy()
    b3.destroy()
    b4.destroy()
    b5.destroy()
    b6.destroy()
    b7.destroy()
    b8.destroy()
    b9.destroy()
    b0.destroy()
    ee = 0


# hàm tạo chức năng của emoji
def bb1():
    mark('e1')
def bb2():
    mark('e2')
def bb3():
    mark('e3')
def bb4():
    mark('e4')
def bb5():
    mark('e5')
def bb6():
    mark('e6')    
def bb7():
    mark('e7')
def bb8():
    mark('e8')
def bb9():
    mark('e9')
def bb0():
    mark('e0')
# tạo button cho từng emoji
def express():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9, b0, ee
    if ee == 0:
        ee = 1
        b1 = tkinter.Button(root, command=bb1, image=emoji_1,
                            relief=tkinter.FLAT, bd=0)
        b2 = tkinter.Button(root, command=bb2, image=emoji_2,
                            relief=tkinter.FLAT, bd=0)
        b3 = tkinter.Button(root, command=bb3, image=emoji_3,
                            relief=tkinter.FLAT, bd=0)
        b4 = tkinter.Button(root, command=bb4, image=emoji_4,
                            relief=tkinter.FLAT, bd=0)
        b5 = tkinter.Button(root, command=bb5, image=emoji_5,
                            relief=tkinter.FLAT, bd=0)
        b6 = tkinter.Button(root, command=bb6, image=emoji_6,
                            relief=tkinter.FLAT, bd=0)
        b7 = tkinter.Button(root, command=bb7, image=emoji_7,
                            relief=tkinter.FLAT, bd=0)
        b8 = tkinter.Button(root, command=bb8, image=emoji_8,
                            relief=tkinter.FLAT, bd=0)
        b9 = tkinter.Button(root, command=bb9, image=emoji_9,
                            relief=tkinter.FLAT, bd=0)    
        b0 = tkinter.Button(root, command=bb0, image=emoji_0,
                            relief=tkinter.FLAT, bd=0)                
        b1.place(x=5, y=248)
        b2.place(x=41, y=248)
        b3.place(x=77, y=248)
        b4.place(x=113, y=248)
        b5.place(x=149, y=248)
        b6.place(x=5, y=284)
        b7.place(x=41, y=284)
        b8.place(x=77, y=284)
        b9.place(x=113, y=284)
        b0.place(x=149, y=284)
    else:
        ee = 0
        b1.destroy()
        b2.destroy()
        b3.destroy()
        b4.destroy()
        b5.destroy()
        b6.destroy()
        b7.destroy()
        b8.destroy()
        b9.destroy()
        b0.destroy()


# tạo emoji button
eBut = tkinter.Button(root, text='emoji',font=('Barlow Condensed Medium',12), command=express)
eBut.place(x=5, y=320, width=60, height=30)


# Online user list
listbox1 = tkinter.Listbox(root)
listbox1.place(x=445, y=0, width=130, height=320)


def users():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=445, y=0, width=130, height=320)
        ii = 0
    else:
        # ẩn thanh điều khiển user đang hoạt động
        listbox1.place_forget()
        ii = 1


# button của user list đang hoạt động 
button1 = tkinter.Button(root, text='Online users',font=('Barlow Condensed Medium',12), command=users)
button1.place(x=480, y=320, width=95, height=30)

# Input Text box
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=350, width=570, height=40)

# gửi message
def send(*args):
    users.append('------GROUP CHAT-------')
    print(chat)
    # Nếu user nhận tin không có trong users, thông báo không ai có thể trò chuyện với bạn
    if chat not in users:
        tkinter.messagebox.showerror(
            'Send error', message='There is nobody to talk to!')
        return

    #nếu user nhận tin là chính mình thì thông báo không thể tự nói chuyện với chính mình
    if chat == user:
        tkinter.messagebox.showerror(
            'Send error', message='Cannot talk with yourself in private!')
        return
    # gửi cho server tin xem người dùng đang nhắn tin với ai cùng với nội dung tin nhắn
    mes = entry.get() + ':;' + user + ':;' + chat
    s.send(mes.encode())
    a.set('')  # sau khi gửi tin nhắn, textbox trở về trống


# Send message button
button = tkinter.Button(root, text='Send',font=('Barlow Condensed Medium',12), command=send)
button.place(x=515, y=353, width=60, height=30)
root.bind('<Return>', send)


# chức năng nhắn tin riêng tư
def private(*args):
    global chat
    # lấy user name
    indexs = listbox1.curselection()
    index = indexs[0]
    if index > 0:
        chat = listbox1.get(index)
        # Thay đổi nhắn tin nhóm thành nhắn tin riêng tư
        if chat == '------GROUP CHAT-------':
            root.title(user)
            return
        ti = user + '  ->  ' + chat
        root.title(ti)


# Ràng buộc tin nhắn riêng tư trên user list
listbox1.bind('<ButtonRelease-1>', private)


# hàm nhận tin nhắn
def recv():
    global users
    while True:
        data = s.recv(1024)
        data = data.decode()
        # Nếu không có lỗi, nghĩa là đã nhận được user list
        try:
            data = json.loads(data)
            users = data
            # user list box GUI
            listbox1.delete(0, tkinter.END)
            number = ('   Users online: ' + str(len(data)))
            listbox1.insert(tkinter.END, number)
            listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
            listbox1.insert(tkinter.END, '------GROUP CHAT-------')
            listbox1.itemconfig(tkinter.END, fg='green')
            for i in range(len(data)):
                listbox1.insert(tkinter.END, (data[i]))
                listbox1.itemconfig(tkinter.END, fg='green')
        except:
            data = data.split(':;')
            data1 = data[0].strip()  # nội dung tin nhắn
            data2 = data[1]  # user name
            data3 = data[2]  # chat (user nhận tin)

            markk = data1.split('：')[1]
            # kiểm tra xem emoji có trong dict không
            if (markk in dict) :
                data4 = '\n' + data2 + '：'  
                if data3 == '------GROUP CHAT-------':
                    if data2 == user:
                        # Nếu đó là chính user, chuyển phông chữ thành màu xanh nước biển
                        listbox.insert(tkinter.END, data4, 'blue')
                        listbox.image_create(tkinter.END, image=dict[markk])
                    else:
                        listbox.insert(tkinter.END, data4,'green')
                        listbox.image_create(tkinter.END, image=dict[markk])
                elif data2 == user or data3 == user:  # nhắn tin là riêng tư
                    listbox.insert(tkinter.END, data4, 'red')
                    listbox.image_create(tkinter.END, image=dict[markk])

            # cài đặt màu chữ
            else:
                data1 = '\n' + data1
                if data3 == '------GROUP CHAT-------':
                    if data2 == user:
                        # Nếu đó là chính user, chuyển phông chữ thành màu xanh nước biển
                        listbox.insert(tkinter.END, data1, 'blue')
                    else:
                        listbox.insert(tkinter.END, data1,
                                       'green')

                elif data2 == user or data3 == user:  # tin nhắn riêng tư
                    listbox.insert(tkinter.END, data1, 'red')
            listbox.see(tkinter.END)  # hiển thị cuối cùng


# bắt đầu nhận tin nhắn
r = threading.Thread(target=recv)
r.start()
# Tkinter GUI
root.mainloop()
s.close()
