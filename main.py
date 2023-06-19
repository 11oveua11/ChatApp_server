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
        self.global_answer = 'unknown'

        # starting server
        self.sqlite = SQLite()
        self.s_srv = socket.create_server(('127.0.0.1', 8698))
        self.s_srv.listen(100)

        while True:

            print('сервер начал слушать, и ждёт подключения')
            while True:
                self.client_socket, address = self.s_srv.accept()
                self.full_msg = ""
                data = self.client_socket.recv(1024)
                    # if data == "":
                    #     break
                self.full_msg += data.decode('utf-8')
                print(self.full_msg)
                answer = self.action_dict[self.full_msg.split()[0]]()
                self.client_socket.send(bytes(answer, 'utf-8'))
                self.client_socket.close()
                # self.client_socket.sendmsg()



    def main_data_handler(self):
        content = 'MAIN DATA FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

    def users_handler(self):
        content = 'USERS FROM SERVER!!!!!!!!'.encode('utf-8')
        self.client_socket.send(content)

    def new_user_handler(self):
        return self.sqlite.create_user(*self.full_msg.split()[1:])



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
            return 'True'
        else:
            return 'False'






if __name__ == "__main__":
    my_server = MyServer()