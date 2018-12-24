import asyncio
import websockets

voc = {
    'name?': 'ACDC',
    'email?': 'acdc@qq.com',
    'gender?': 'n'
}


async def myclient():
    try:
        async with websockets.connect('ws://localhost:8765')as websocket:
            while (True):
                try:
                    question = await websocket.recv()
                    print('Received: ' + question)
                    print('Answering with: ' + voc[question])
                    await  websocket.send(voc[question])

                except websocket.exceptions.ConnectionClosed:
                    print('Connection closed !Error! ')
                    break

                except KeyError:
                    print('Malformed request: ' + question)
                    break

    except ConnectionRefusedError:
        print('Connection Refused!')


asyncio.get_event_loop().run_until_complete(myclient())
