import time

try:
    import ujson as json
except ImportError:
    import json

from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from logging import Logger, DEBUG
from pprint import pprint

log = Logger("client_main")


class World:
    data = []

    auth = False

    def handler(self, data):
        if data['type'] == 'tick':
            self.data = data['data']
        elif data['type'] == 'auth_ok':
            self.auth = True


world = World()


class Pinger(Thread):
    def __init__(self, connection):
        self.connection = connection
        log.debug("Pinger Init")
        super().__init__(target=self.run)

    def run(self):
        while True:
            self.connection.send({"request": "ping", "data": {}})
            time.sleep(2)
            log.debug("Pinging server")


class Connection(Thread):
    total_debug = False

    def __init__(self, address=('localhost', 8956), handler=None, total_debug=False, auth=()):
        self.address = address
        self.socket = socket(AF_INET, SOCK_DGRAM)

        self.handler = handler

        self.send({"request": "connect"})

        self.pinger = Pinger(self)
        self.pinger.start()

        self.total_debug = total_debug

        if auth:
            self.connect(*auth)

        super().__init__(target=self.run)
        if self.handler:
            self.start()

    def send(self, data):
        self.socket.sendto(json.dumps(data).encode('utf-8'), self.address)
        log.debug("Sending data to server.")
        if self.total_debug:
            print("----------- DATA -----------")
            pprint(data)
            print("-------- END OF DATA -------")
        time.sleep(0.3)

    def action(self, action, data=None):
        log.debug(f"Sending action {action} to server")
        self.send({'action': action, 'data': data})

    def eval(self, command):
        log.debug("Sending `eval` to server")
        self.send({'type': 'get_eval', 'data': command})
        while True:
            r = self.recv()
            print(r)
            if r['type'] == 'eval':
                return r['data']
            self.handler(r)

    def recv(self):
        return json.loads(self.socket.recvfrom(8024)[0].decode('utf-8'))

    def disconnect(self):
        log.debug("Sending disconnect to server")
        self.send({"request": "disconnect"})

    def connect(self, user, passw):
        self.send({'type': 'auth', 'data': {'user': user, 'password': passw}})

    def run(self):
        if not self.handler:
            raise NotImplementedError('handler must be function')
        while True:
            self.handler(self.recv())

    def __del__(self):
        self.disconnect()


if __name__ == '__main__':
    from ptpython.repl import embed

    connection = Connection(total_debug=True, handler=world.handler, auth=("admin", "1234"))


    def dis_dbg():
        connection.total_debug = False


    def reconnect():
        return Connection(total_debug=True, handler=world.handler, auth=("admin", "1234"))


    dis_dbg()

    embed(globals(), locals())
    connection.disconnect()
