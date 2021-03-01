import json
import aiohttp
import asyncio


# wss://webuilders.cz/api/v1/counter/connect

async def main():
    session = aiohttp.ClientSession()

    while True:
        try:
            async with session.ws_connect('wss://webuilders.cz/api/v1/counter/connect', heartbeat=5.0) as ws:
                async for msg in ws:
                    data = json.loads(msg.data)
                
                    if data['type'] == 'MarketConfig':
                        for market in data['markets']:
                            await ws.send_json({'type': 'MarketRegister', 'marketId': market['id']})
                            await asyncio.sleep(0.1)
                    else:
                        print(msg)
        except aiohttp.ClientError:
            print('Reconnecting...')
            await asyncio.sleep(5)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass