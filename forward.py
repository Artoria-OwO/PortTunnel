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

        self.remote = socket.create_connection((targethost, targetport))

        self.local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.local.bind(("0.0.0.0", self.port))

        self.local.listen(10)

        print("local port:" + str(port) + " remote address:" + targethost + ":" + str(self.targetport))

    def run(self):
        while True:
            local, _ = self.local.accept()

            remote = socket.create_connection((self.targethost, self.targetport))

            PipeThread(local, remote).start()

            PipeThread(remote, local).start()


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])

        targethost = sys.argv[2]

        targetport = int(sys.argv[3])

        Forwarding(port, targethost, targetport).start()

    except (ValueError, IndexError):
        print('Usage: %s port targethost targetport' % sys.argv[0])
        sys.exit(1)
