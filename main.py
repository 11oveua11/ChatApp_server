# from flask import Flask
import socket

class MyServer():
    def __init__(self):
        self.action_dict = {'main_data': self.main_data_handler,
                            'users': self.users_handler,
                            'dialog': self.dialog_handler,
                            'new_msg': self.new_msg_handler

                            }

        # starting server
        self.s_srv = socket.create_server(('127.0.0.1', 1234))
        self.s_srv.listen(100)
        while True:
            print('working..')
            self.client_socket, address = self.s_srv.accept()
            self.client_socket.send(bytes("Добро пожаловать на сервер!!!", 'utf-8'))
            self.req_data = self.client_socket.recv(1024).decode('utf-8')
            print(self.req_data)
            #self.client_socket.send(bytes(self.req_data, 'utf-8'))
            self.action_dict[self.req_data]()
            # self.client_socket.sendmsg()



    def main_data_handler(self):
        content = 'MAIN DATA FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

    def users_handler(self):
        content = 'USERS FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

    def dialog_handler(self):
        content = 'dialog FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

    def new_msg_handler(self):
        content = 'new msg FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)



if __name__ == "__main__":
    my_server = MyServer()