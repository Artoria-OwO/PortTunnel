import socket
import sys
import threading


class PipeThread(threading.Thread):
    def __init__(self, source, target):
        threading.Thread.__init__(self)
        self.source = source
        self.target = target

    def run(self):
        while True:
            try:
                data = self.source.recv(2048)
                if not data: break
                self.target.send(data)
            except:
                continue


class Forwarding(threading.Thread):
    def __init__(self, port, targethost, targetport):
        threading.Thread.__init__(self)

        self.port = port

        self.targethost = targethost

        self.targetport = targetport

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind((targethost, targetport if targetport != -1 else 0))

        _, self.targetport = self.sock.getsockname()

        self.sock.listen(10)

        print("local port:" + str(port) + " remote address: " + targethost + ":" + str(self.targetport))

    def run(self):
        while True:
            client_fd, client_addr = self.sock.accept()

            target_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            target_fd.connect(("", self.port))

            PipeThread(target_fd, client_fd).start()

            PipeThread(client_fd, target_fd).start()


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])

        targethost = sys.argv[2]

        targetport = int(sys.argv[3]) if sys.argv.__len__() >= 4 else -1

        Forwarding(port, targethost, targetport).start()

    except (ValueError, IndexError):
        print('Usage: %s port targethost [targetport]' % sys.argv[0])
        sys.exit(1)
