import socket
import asyncio
from threading import Thread
import time
from ast import literal_eval

import globals as gl

#client.sendto(b"register/2", ('localhost', 56565))

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind(('localhost', 0))
        self.addr=self.client.getsockname()
        self.loop = asyncio.new_event_loop()
        self.running = False

    def start(self):
        """Запускает фоновый асинхронный обработчик"""
        self.running = True
        Thread(target=self._run_async_loop, daemon=True).start()

    def _run_async_loop(self):
        """Запускает asyncio loop в отдельном потоке"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._listen_server())

    async def _listen_server(self):
        """Асинхронно слушает сообщения"""
        while self.running:
            try:
                data, addr = await self.loop.run_in_executor(None, self.client.recvfrom, 1024)
                data = data.decode('utf-8')
                print(f"{data}-----{addr}")
                words=data.split('/')
                if words[0] == 'success':
                    if words[1] == 'start_round':
                        gl.game_state = 'start_round'
                    elif words[1] == 'end_round':
                        gl.game_state = 'start_pause'
                elif words[0] == 'winner':
                    if words[1] != "None":
                        gl.winner_name = words[1]
                        gl.winner_addr = literal_eval(words[2])
                        gl.winner_choice = words[3]
                    else:
                        gl.winner_choice = words[1]
            except Exception as e:
                print(f"Receive error: {e}")
                break

    def send(self, message: str):
        """Синхронная отправка сообщения"""
        self.client.sendto(message.encode('utf-8'), ('localhost', 56565))

    def stop(self):
        """Остановка клиента"""
        self.running = False
        self.client.close()
