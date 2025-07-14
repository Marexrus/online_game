import asyncio

async def main():
    loop = asyncio.get_event_loop()  # Получаем текущий event loop
    print("Event loop:", loop)

asyncio.run(main())