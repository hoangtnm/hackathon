from os import getenv

import eventlet
import socketio

HOST = getenv('SOCKET_HOST', '0.0.0.0')
PORT = getenv('SOCKET_PORT', 7642)
NAMESPACE = '/ns'

sio = socketio.Server(async_mode='eventlet')
app = socketio.Middleware(sio)


@sio.on('connect', namespace=NAMESPACE)
def connect(sid, environ):
    print(f'Connection established with {sid}')


@sio.on('message', namespace=NAMESPACE)
def message(sid, data):
    # print('.' * 70)
    # psize = len(data)
    # print('Received data at {}. Packet size in bytes: {} ({})'.format(
    #     get_time(),
    #     psize,
    #     byte_to_text(psize)
    # ))
    # print(':' * 70)
    pass


def start_server():
    try:
        print(f'SocketIO server is started at ws://{HOST}:{PORT}')
        eventlet.wsgi.server(
            eventlet.listen((HOST, PORT)),
            app,
            log_output=False
        )
    except Exception as err:
        print(err)


if __name__ == '__main__':
    start_server()
