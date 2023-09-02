import asyncio
from websockets import connect
import aiofiles
import httpx, json, time
from datetime import datetime as dt


async def binanceOrderbookDownload(pair):
    ws_url = f"wss://stream.binance.com:9443/ws/{pair.lower()}@depth"
    rest_url = "https://api.binance.com/api/v3/depth"

    params = {
        "symbol": pair,
        "limit": 10,
    }
    today = dt.now().date()

    async with httpx.AsyncClient() as client:
        snapshot = await client.get(rest_url, params=params)
    
    snapshot = snapshot.json()
    snapshot["time"] = time.time()

    async with aiofiles.open(f"{pair.lower()}-snapshots-{today}", mode='a') as f:
        await f.write(json.dumps(snapshot) + '\n')

    async with connect(ws_url) as websocket:
        while True:
            data = await websocket.recv()
            print(data)
            async with aiofiles.open(f"{pair.lower()}-updates-{today}.txt", mode='a') as f:
                await f.write(data + '\n')


#asyncio.run(binanceOrderbookDownload('BTCUSDT'))

