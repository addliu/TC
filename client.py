import socket, sys, signal
from window import Window
from threading import Thread
from clint.textui import colored


class Client(Window):
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password + '\n'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print("host:", self.host, "port:", self.port)
        self.sock.connect((self.host, self.port))
        self.sendMsg(self.sock, self.password)
        message = self.recvMsg(self.sock, '\n')
        print(message)
        if message.replace('\n', '') != '~q':
            username = input(colored.yellow("Enter your username: "))
            Thread(target=self.sends, args=(username,)).start()
            Thread(target=self.recvs, args=('\n',)).start()
        else:
            sys.exit(0)

    def sends(self, username):
        while True:
            message = input()
            print("\033[A             \033[A")
            print(colored.yellow("<me>"), colored.magenta(message))
            if message == '~q':
                message += '\n'
                self.sendMsg(self.sock, message)
                self.sock.shutdown(socket.SHUT_WR)
                break
            message += "\n"
            message = '<' + username + '>' + message
            self.sendMsg(self.sock, message)

    def recvs(self, delimeter):
        while True:
            message = self.recvMsg(self.sock, delimeter)
            if message.replace('\n', '') == '~q':
                self.sock.close()
                break
            message = message.replace('\n', '')
            index = message.index('>')
            print(colored.yellow(message[0:index + 1]), colored.red(message[index + 1:]))


def main(argv):
    client = Client(argv[0], 1060, argv[1])
    client.start()
