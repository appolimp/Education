import socket
import time
from pprint import pprint


class ClientError(Exception):
    def __init__(self, name):
        self.name = name


class Client:

    @staticmethod
    def data_get_valid(data):

        return True

    @staticmethod
    def get_process(data):
        status, *lines = data.rstrip().split('\n')
        result = {}
        for line in lines:
            key, value, timestamp = line.split()
            result[key] = result.get(key, []) + [(int(timestamp), float(value))]
        return result

    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)

    def get(self, key):
        try:
            self.sock.sendall(f'get {key}\n'.encode('utf8'))
            data = self.sock.recv(1024).decode('utf8')
        except socket.error:
            raise ClientError('bad connection')

        if not Client.data_get_valid(data):
            raise ClientError('no valid data')

        return Client.get_process(data)

    def put(self, key: str, value: float, timestamp: int = None) -> None:
        try:
            self.sock.sendall(f'put {key} {value} {timestamp or int(time.time())}\n'.encode('utf8'))
            data = self.sock.recv(1024).decode('utf8')
        except socket.error:
            raise ClientError('bad connection')

        if data != 'ok\n\n':
            raise ClientError('no valid data\n')


if __name__ == '__main__':
    client = Client("127.0.0.1", 8181, timeout=15)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.memory", 4200000)
    print(client.get("*"))
    # pprint(client.get("125"))


