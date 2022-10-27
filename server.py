import socket
import threading
import queue
import json
import time
import os
import os.path
import sys

IP = ''
PORT = 50007
queue = queue.Queue()                   # lưu trữ tin nhắn của user trong hàng đợi
users = []                              # lưu thông tinh user đang hoạt động  [conn, user, addr]
lock = threading.Lock()                 # multitreading lock (khóa đa luồng)


#thêm user mới vào danh sách user đang hoạt động

def onlines():
    online = []
    for i in range(len(users)):
        online.append(users[i][1])
    return online


class ChatServer(threading.Thread):
    global users, queue, lock

    # hàm khởi tạo
    def __init__(self, port):
        threading.Thread.__init__(self)
        # self.setDaemon(True)
        self.ADDR = ('', port)
        # self.PORT = port
        os.chdir(sys.path[0])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #tạo socket mới với ip4 và tcp/ip
        # self.conn = None
        # self.addr = None

    # hàm nhận tin nhắn từ client
    def tcp_connect(self, conn, addr):
        # nhận user name 
        user = conn.recv(1024)
        user = user.decode()

        # kiểm tra tên user đã có trong danh sách chưa, nếu đã có thì thêm '_2'
        for i in range(len(users)):
            if user == users[i][1]:
                print('User already exist')
                user = '' + user + '_2'

        if user == 'no':
            user = addr[0] + ':' + str(addr[1])
        users.append((conn, user, addr))
        # in ra tên user mới
        print(' New connection:', addr, ':', user, end='')
        # làm mới user list
        d = onlines()
        self.recv(d, addr)
        try:
            while True:
                data = conn.recv(1024)
                data = data.decode()
                self.recv(data, addr)
            conn.close()
        except:
            print(user + ' Connection lose')
            # xóa user khỏi userlist và chat room
            self.delUsers(conn, addr)
            conn.close()

    # hàm xóa user
    def delUsers(self, conn, addr):
        a = 0
        for i in users:
            if i[0] == conn:
                users.pop(a)
                print(' Remaining online users: ',
                      end='')
                d = onlines()
                self.recv(d, addr)
                # in ra danh sách người dùng còn hoạt động
                print(d)
                break
            a += 1

    # hàm lưu trữ ip, data, addr vào queue
    def recv(self, data, addr):
        lock.acquire()
        try:
            queue.put((addr, data))
        finally:
            lock.release()

    # gửi tin nhắn trong queue cho tất cả người dùng
    def sendData(self):
        while True:
            if not queue.empty():
                data = ''
                # lấy ra phần tử đầu tiên trong hàng đợi
                message = queue.get()
                # nếu tin nhắn là một string (message[0] là addr, message[1] là data)
                if isinstance(message[1], str):
                    for i in range(len(users)):
                        # user [i][1] là username, users [i][2] là addr
                        for j in range(len(users)):
                            # kiểm tra xem tin nhắn đến từ người dùng nào
                            if message[0] == users[j][2]:
                                print(
                                    ' message is from user[{}]'.format(j))
                                data = ' ' + users[j][1] + '：' + message[1]
                                break
                        users[i][0].send(data.encode())
                # data = data.split(':;')[0]
                #nếu tin nhắn là một list
                if isinstance(message[1], list):
                    #nếu là list thì gửi trực tiếp
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            users[i][0].send(data.encode())
                        except:
                            pass

    def run(self):

        self.s.bind(self.ADDR)
        self.s.listen(5)
        print('Chat server starts running...')
        q = threading.Thread(target=self.sendData)
        q.start()
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr))
            t.start()
        self.s.close()


if __name__ == '__main__':
    cserver = ChatServer(PORT)
    cserver.start()

    while True:
        time.sleep(1)
        if not cserver.is_alive():
            print("Chat connection lost...")
            sys.exit(0)
