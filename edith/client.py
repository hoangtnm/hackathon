from os import getenv

import eventlet
import socketio

HOST = getenv('HOST', '0.0.0.0')
PORT = getenv('PORT', 7642)
NAMESPACE = '/ns'

sio = socketio.Client()


def start_client():
    try:
        sio.connect(f'ws://{HOST}:{PORT}', namespaces=[NAMESPACE])
        sio.wait()
    except Exception as err:
        print('Error while trying to start socket client:')
        print(err)


if __name__ == '__main__':
    start_client()
