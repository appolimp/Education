import asyncio


def valid_input_req(data):
    return True


def put(key, value, timestamp):
    big_data.setdefault(key, {})
    big_data[key][timestamp] = value
    return 'ok\n\n'


def get(key):

    def prepare_data(key):
        out = []
        for timestamp, value in sorted(big_data[key].items()):
            out.append(f'{key} {value} {timestamp}')
        return '\n'.join(out)

    response = ['ok']
    if key == '*':
        for key in big_data:
            response.append(prepare_data(key))
    elif key not in big_data:
        pass
    else:
        response.append(prepare_data(key))
    return '\n'.join(response)+'\n\n'


def process_data(request):
    if not valid_input_req(request):
        return None

    comma, *data = request.rstrip().split()
    if comma == 'put':
        return put(*data)
    else:
        return get(*data)


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        request = data.decode('utf-8')
        print(f'Получен запрос: {ascii(request)}')

        resp = process_data(request)
        print(f'Отправлен ответ {ascii(resp)}')
        self.transport.write(resp.encode('utf-8'))


big_data = {}

loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8181)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

