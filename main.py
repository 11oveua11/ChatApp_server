# from flask import Flask
import socket
import sqlite3

class MyServer():
    def __init__(self):
        self.action_dict = {'main_data': self.main_data_handler,
                            'users': self.users_handler,
                            'new_user': self.new_user_handler,
                            'dialog': self.dialog_handler,
                            'new_msg': self.new_msg_handler


                            }

        # starting server
        self.sqlite = SQLite()
        self.s_srv = socket.create_server(('127.0.0.1', 1234))
        self.s_srv.listen(100)
        while True:

            print('working..')
            self.client_socket, address = self.s_srv.accept()
            with self.client_socket:
                self.client_socket.send(bytes("Добро пожаловать на сервер!!!", 'utf-8'))
                self.req_data = self.client_socket.recv(1024).decode('utf-8')
                print(self.req_data)
                #self.client_socket.send(bytes(self.req_data, 'utf-8'))
                self.action_dict[self.req_data.split()[0]]()
                # self.client_socket.sendmsg()



    def main_data_handler(self):
        content = 'MAIN DATA FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

    def users_handler(self):
        content = 'USERS FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

    def new_user_handler(self):
        answer = self.sqlite.create_user(*self.req_data.split()[1:])
        self.client_socket.send(answer.encode('utf-8'))


    def dialog_handler(self):
        content = 'dialog FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

    def new_msg_handler(self):
        content = 'new msg FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

class SQLite():
    def __init__(self):
        self.db = sqlite3.connect('chatapp.db')
        self.curs = self.db.cursor()

        self.curs.execute('''CREATE TABLE IF NOT EXISTS users (
        login TEXT PRIMARY KEY,
        name TEXT ,
        pass TEXT,
        gender INTEGER DEFAULT 0
        )''')
        self.db.commit()

    def create_user(self, username, password, gender):
        self.curs.execute("SELECT login FROM users WHERE login = '{username}'")
        result = self.curs.fetchone()
        if not self.curs.fetchone():
            self.curs.execute(f"INSERT INTO users VALUES (?, ?, ?)", (username, password, gender))
            self.db.commit()
            return ("User created!")
        else:
            return ("Error! User already exists!")






if __name__ == "__main__":
    my_server = MyServer()