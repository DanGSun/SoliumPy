from server.server import Server
from traceback import print_exc

if __name__ == '__main__':
    try:
        s = Server()
        s.run()
    except Exception as _:
        print_exc()

    input()
