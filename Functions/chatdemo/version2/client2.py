import asyncio
import websockets

end_point = 'ws://service.recommendersystem.com/recsys2-course/engine'

voc = {

    'Author name': "Andrea Galloni",
    'Author email': 'andreagalloni[92][at]gmail[dot]com',
    'Author id': 'JGNBMW'

}


async def myclient():
    try:
        async with websockets.connect(end_point) as websocket:
            while (True):
                try:
                    quesion = await websocket.recv()
                    print('Received :' + quesion)
                    print("Answering with: " + voc[quesion])
                    await websocket.send(voc[quesion])
                except websockets.exceptions.ConnectionClosed:
                    print('Connection Closed!')
                except KeyError:
                    print('Malformed request: ' + quesion)
                    break
    except ConnectionRefusedError:
        print('Connection Refused!')


asyncio.get_event_loop().run_until_complete(myclient())
