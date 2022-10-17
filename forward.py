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
    def __init__(self, targethost, targetport):
        threading.Thread.__init__(self)

        self.targethost = targethost

        self.targetport = targetport

        self.remote = socket.create_connection((targethost, targetport))

        self.local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.local.bind(("0.0.0.0", 0))

        self.local.listen(10)

        print("local port:" + str(self.local.getsockname()[1]) + " remote address:" + targethost + ":" + str(
            self.targetport))

    def run(self):
        while True:
            local, _ = self.local.accept()

            remote = socket.create_connection((self.targethost, self.targetport))

            PipeThread(local, remote).start()

            PipeThread(remote, local).start()


if __name__ == '__main__':
    try:
        targethost = sys.argv[1]

        targetport = int(sys.argv[2])

        Forwarding(targethost, targetport).start()

    except (ValueError, IndexError):
        print('Usage: %s targethost targetport' % sys.argv[0])
        sys.exit(1)
