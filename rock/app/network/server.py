import datetime
import socket
import asyncio
from ast import literal_eval


def find_instance(field_name: str, target_value, instances: list) -> object:
    """
    Находит первый экземпляр в списке, у которого поле field_name равно target_value.

    Args:
        field_name (str): Название поля для поиска (например, 'addr', 'name').
        target_value: Значение поля для сравнения.
        instances (list): Список экземпляров класса.

    Returns:
        object: Первый найденный экземпляр или None, если не найден.
    """
    for instance in instances:
        if getattr(instance, field_name) == target_value:
            return instance
    return None


class User:
    def __init__(self, addr,name):
        self.addr = addr
        self.name = name
        self.room = None
        self.choice = None


class Room:
    def __init__(self,name):
        self.name = name
        self.players=[]

        self.room_size=2

        self.players_addr=[]

    def player_join(self, player):
        self.players.append(player)
        self.players_addr.append(player.addr)

    def check_fill(self):
        if len(self.players) == self.room_size:
            return True
        else:
            return False

    def check_choice(self):
        if self.check_fill():
            for player in self.players:
                if not player.choice:
                    return False
            return True
        else:
            return False

    def check_winer(self):
        # Проверяем валидность выборов
        valid_choices = {'rock', 'paper', 'scissors'}
        for user in self.players:
            if user.choice not in valid_choices:
                raise ValueError(f"Invalid choice: {user.choice}. Must be one of {valid_choices}")

        # Собираем статистику по выборам
        choices = [user.choice for user in self.players]
        unique_choices = set(choices)

        # Если все выбрали одинаково - ничья
        if len(unique_choices) == 1:
            return []

        # Определяем победную комбинацию
        if 'rock' in unique_choices and 'scissors' in unique_choices and 'paper' in unique_choices:
            # Все три варианта есть - ничья
            return []
        elif 'rock' in unique_choices and 'scissors' in unique_choices:
            # Rock beats scissors
            winning_choice = 'rock'
        elif 'scissors' in unique_choices and 'paper' in unique_choices:
            # Scissors beat paper
            winning_choice = 'scissors'
        elif 'paper' in unique_choices and 'rock' in unique_choices:
            # Paper beats rock
            winning_choice = 'paper'
        else:
            # Неожиданная комбинация (теоретически невозможна после проверок выше)
            return []

        # Возвращаем всех пользователей с победным выбором
        return [user for user in self.players if user.choice == winning_choice]



class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.server.setblocking(False)
        self.run = False

        self.users = []
        self.rooms = []
        self.rooms.append(Room('test_room'))

    async def start(self):
        self.server.bind(('localhost', 56565))
        self.run = True

        self.loop = asyncio.get_running_loop()
        print("Server has been started")
        await self.update()

    async def check_data(self,data, addr):
        data=data.decode('utf-8')
        words=data.split('/')
        if words[0] == 'register':
            await self.register(words, addr)
        if words[0] == 'join':
            await  self.join_to_room(words,addr)
        elif words[0] == 'round':
            await self.round(words,addr)


    async def update(self):
        while self.run:
            data, addr = await self.loop.create_task(self.take_data())
            if data:
                print(f"{data.decode('utf-8')}__________{addr}__________{datetime.datetime.now().time()}")
                await self.check_data(data, addr)

        self.server.close()

    async def register(self,words, addr):
        self.users.append(User(words[1],words[2]))
        print(f"User {words[1]} registration with name {words[2]}")

        self.server.sendto(b'success/registration', addr)

    async def join_to_room(self,words, addr):
        user = find_instance('addr',words[1], self.users)
        user.room=words[2]

        room = find_instance('name',words[2], self.rooms)
        room.player_join(user)
        check_fill=room.check_fill()
        if check_fill:
            self.broadcast(room.players_addr,b'success/start_round')
        self.server.sendto(b'success/join', addr)

    async def round(self,words,addr):
        user = find_instance('addr', words[1], self.users)
        user.choice = words[2]
        room = find_instance('name', user.room, self.rooms)
        if room.check_choice():
            winner = room.check_winer()
            if winner:
                print(f"WINNER-----{winner[0].name}----")
                self.broadcast(room.players_addr, f"winner/{winner[0].name}/{winner[0].addr}/{winner[0].choice}".encode('utf-8'))
                if room.check_fill():
                    self.broadcast(room.players_addr, b'success/end_round')
            else:
                print(f"WINNER-----None----")
                self.broadcast(room.players_addr, f"winner/None".encode('utf-8'))
                if room.check_fill():
                    self.broadcast(room.players_addr, b'success/end_round')
        else:
            print("Не все игроки выбрали")

    async def take_data(self):
         data, addr = self.server.recvfrom(1024)
         return data,addr

    def broadcast(self,addrs,data):
        for addr in addrs:
            self.server.sendto(data, literal_eval(addr))
async def main():
    server = Server()
    await server.start()

asyncio.run(main())