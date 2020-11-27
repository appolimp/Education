import socket
import asyncio


# переменная response хранит строку возвращаемую сервером, если вам для
# тестирования клиента необходим другой ответ, измените ее
response = b'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'


async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    print('Соединение установлено:', addr)

    data = await reader.read(1024)
    request = data.decode('utf-8')
    print(f'Получен запрос: {ascii(request)}')
    print(f'Отправлен ответ {ascii(response.decode("utf-8"))}')
    writer.write(response)
    # writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
asyncio.run(server.wait_closed())
loop.close()