import json
import socket
import hashlib
import base64
import struct
import urllib


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

    # def parse_data(self, msg):
    #
    #     print('msg-1: ' + msg[1])
    #     print(msg.encode('utf-8'))
    #     print('parse target: ' + msg)
    #     v = (ord(msg[1])) & 0x7f
    #     print("v : " + str(v))
    #     # v = data & 0x7f
    #     if v == 0x7e:
    #         p = 4
    #     elif v == 0x7f:
    #         p = 10
    #     else:
    #         p = 2
    #     mask = msg[p: p + 4]
    #     data = msg[p + 4:]
    #     print(type(msg))
    #     print('mask: ' + mask)
    #     print('data: ' + data)
    #     # str1 = ''.join([chr(ord(n) ^ ord(mask[i % 4])) for i, n in enumerate(data)])
    #     str_re = ''
    #     for i, d in enumerate(data):
    #         print('d: ' + d)
    #         print('mask : ' + mask[i % 4])
    #         print('ord d: ' + chr(ord(d)))
    #         print(str(i) + ' |position: ' + chr(ord(d) ^ ord(mask[i % 4])))
    #         str_re = str_re + chr(ord(d) ^ ord(mask[i % 4]))
    #     return str_re
    def message_decode(self, data):
        HEADER, = struct.unpack("!H", data[:2])
        data = data[2:]

        FIN = (HEADER >> 15) & 0x01
        RSV1 = (HEADER >> 14) & 0x01
        RSV2 = (HEADER >> 13) & 0x01
        RSV3 = (HEADER >> 12) & 0x01
        OPCODE = (HEADER >> 8) & 0x0F
        MASKED = (HEADER >> 7) & 0x01
        LEN = (HEADER >> 0) & 0x7F

        if OPCODE == 8:
            return (False, False)

        if LEN == 126:
            LEN, = struct.unpack("!H", data[:2])
            data = data[2:]
        elif LEN == 127:
            LEN, = struct.unpack("!4H", data[:8])
            data = data[8:]

        if MASKED:
            MASK = struct.unpack("4B", data[:4])
            data = data[4:]
        else:
            return (False, False)

        payload = ""
        for i, c in enumerate(data):
            payload += chr(c ^ MASK[i % 4])

        payload = urllib.parse.unquote(payload)
        try:
            _data = json.loads(payload)

            if _data.get("where", -1) == -1 or _data.get("data", -1) == -1:
                raise Exception  # empty area detected, raise exception
        except:
            _data = {"where": "null", "data": {}}

        return (_data["where"], _data["data"])

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

    org_rece = clientSocket.recv(2048)
    receivedData = str(org_rece)

    print('receiveData: ' + receivedData)
    tem.send_vali(clientSocket=clientSocket, receivedData=receivedData)
    while True:
        print('connect ended===============')
        org_rece = clientSocket.recv(2048)
        print(org_rece)
        receivedData = str(org_rece)
        print(org_rece.decode('iso-8859-1'))
        # text = tem.parse_data(msg=receivedData)
        text, te2 = tem.message_decode(data=receivedData)
        print(text)
        print(te2)
        print("parse data: " + text)
        tem.sendMessage(clientSocket=clientSocket, message=text)
