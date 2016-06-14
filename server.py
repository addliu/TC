import socket
import sys
from threading import Thread

from room import Room


class Server(Room):
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.register_clients = []

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(3)

        def chat(sc):
            while True:
                message = self.recvMsg(sc, '\n')
                if not message:
                    break
                if message.replace('\n', '') == '~q':
                    self.sendMsg(sc, message)
                    break
                print(message.replace('\n', ''))
                self.send_to_all_client(message, sc)
            self.deregister_client(sc)
            sc.close()

        while True:
            sc, peeraddr = self.sock.accept()
            message = self.recvMsg(sc, '\n')
            if message.replace('\n', '') == self.password:
                self.sendMsg(sc, 'q\n')
                self.register_client(sc)
                Thread(target=chat, args=(sc,)).start()
            else:
                self.sendMsg(sc, '~q\n')
                sc.close()

    def register_client(self, sc):
        if sc not in self.register_clients:
            self.register_clients.append(sc)

    def send_to_all_client(self, message, sc):
        for sock in self.register_clients:
            if sock is not sc:
                sock.sendall(message.encode())

    def deregister_client(self, sc):
        if sc in self.register_clients:
            self.register_clients.remove(sc)


def main(argv):
    server = Server(argv[0], 1060, argv[1])
    try:
        server.start()
    except KeyboardInterrupt:
        print("Ok! stopping the server!")
        sys.exit(0)
