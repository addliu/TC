class Window(object):
    def sendMsg(self, sock, message):
        sock.sendall(message.encode())

    def recvMsg(self, sock, delimeter):
        message = b""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            message += data
            if delimeter in data.decode():
                break
        # return message.decode()
        return message.decode()

