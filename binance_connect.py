import asyncio
from binance import AsyncClient, BinanceSocketManager
from config import *


async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    ts = bm.book_ticker_socket()

    async with ts as tscm:
        while True:
            res = await tscm.recv()
            if res['s'] in cotirs:
                cotirs[res['s']] = (float(res['b']), float(res['a']))
                print(cotirs)


def start_listening():
    asyncio.Task(main())
