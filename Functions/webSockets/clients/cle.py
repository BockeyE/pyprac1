from websocket import create_connection

ws = create_connection("ws://192.168.3.180:9985/api/v1/streams/valid_transactions")

i = 1
while (i < 15):
    print('===')
    # ws.send("send Hello, World from client:  " + str(i))  ##发送消息
    print(' i have send something')
    result = ws.recv()  ##接收消息
    print('===')
    print('received msg : ' + result)
    if result:
        i += 1

        continue
