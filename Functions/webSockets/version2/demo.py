import socket
import hashlib
import base64
import struct


class tem(object):
    def __init__(self):
        pass

    def send_vali(self, clientSocket, receivedData):
        entities = receivedData.split("\\r\\n")
        Sec_WebSocket_Key = entities[12].split(":")[1].strip() + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        print("key ::", Sec_WebSocket_Key)
        response_key = base64.b64encode(hashlib.sha1(bytes(Sec_WebSocket_Key, encoding="utf8")).digest())
        response_key_str = str(response_key)
        response_key_str = response_key_str[2:30]
        print('resp key : ' + response_key_str)
        response_key_entity = "Sec-WebSocket-Accept: " + response_key_str + "\r\n"
        clientSocket.send(bytes("HTTP/1.1 101 Web Socket Protocol Handshake\r\n", encoding="utf8"))
        clientSocket.send(bytes("Upgrade: websocket\r\n", encoding="utf8"))
        clientSocket.send(bytes(response_key_entity, encoding="utf8"))
        clientSocket.send(bytes("Connection: Upgrade\r\n\r\n", encoding="utf8"))
        print("send the hand shake data")

    def parse_data(self, msg):
        print('parse target: ' + msg)
        v = (ord(msg[1])) & 0x7f
        # v = data & 0x7f
        if v == 0x7e:
            p = 4
        elif v == 0x7f:
            p = 10
        else:
            p = 2
        mask = msg[p: p + 4]
        data = msg[p + 4:]
        print(type(msg))
        print('mask: ' + mask)
        print('data: ' + data)
        return ''.join([chr(ord(n) ^ ord(mask[k % 4])) for k, n in enumerate(data)])

    # 发送websocket server报文部分
    def sendMessage(self, clientSocket, message):
        msgLen = len(message)
        backMsgList = []
        backMsgList.append(struct.pack('B', 129))

        if msgLen <= 125:
            backMsgList.append(struct.pack('b', msgLen))
        elif msgLen <= 65535:
            backMsgList.append(struct.pack('b', 126))
            backMsgList.append(struct.pack('>h', msgLen))
        elif msgLen <= (2 ^ 64 - 1):
            backMsgList.append(struct.pack('b', 127))
            backMsgList.append(struct.pack('>h', msgLen))
        else:
            print("the message is too long to send in a time")
            return
        message_byte = bytes()
        for c in backMsgList:
            message_byte += c
        message_byte += bytes(message, encoding="utf8")
        clientSocket.send(message_byte)


if __name__ == "__main__":
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ("127.0.0.1", 8124)
    serverSocket.bind(host)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.listen(5)
    print("server running")
    tem = tem()
    print("getting connection")
    # 在这个accept 阻塞
    clientSocket, addressInfo = serverSocket.accept()

    print("get connected")
    receivedData = str(clientSocket.recv(2048))
    # print(receivedData)
    print('receiveData: ' + receivedData)
    tem.send_vali(clientSocket=clientSocket, receivedData=receivedData)
    while True:
        receivedData = str(clientSocket.recv(2048))
        text = tem.parse_data(msg=receivedData)
        print("parse data: " + text)
        tem.sendMessage(clientSocket=clientSocket, message=text)
