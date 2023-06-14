# from flask import Flask
import socket

class MyServer():
    def __init__(self):
        self.action_dict = {'main_data': self.main_data_handler

                            }

        # starting server
        self.server = socket.create_server(('127.0.0.1', 5000))
        self.server.listen(100)
        while True:
            print('working..')
            self.client_socket, address = self.server.accept()
            self.req_data = self.client_socket.recv(1024).decode('utf-8')
            print(self.req_data)
            self.action_dict[self.req_data]()

            print('shut....')

    def main_data_handler(self, req):
        content = 'MAIN DATA FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)




if __name__ == "__main__":
    my_server = MyServer()