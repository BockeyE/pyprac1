import socket
import hashlib
import base64
import struct

if __name__ == "__main__":
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ("127.0.0.1", 8124)
    serverSocket.bind(host)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.listen(5)
    print("server running")
    while True:
        print("getting connection")
        # 在这个accept 阻塞
        clientSocket, addressInfo = serverSocket.accept()

        print("get connected")
        receivedData = str(clientSocket.recv(2048))
        # print(receivedData)
        print('receiveData: '+receivedData)
        entities = receivedData.split("\\r\\n")
        Sec_WebSocket_Key = entities[12].split(":")[1].strip() + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        print("key ", Sec_WebSocket_Key)
        response_key = base64.b64encode(hashlib.sha1(bytes(Sec_WebSocket_Key, encoding="utf8")).digest())
        response_key_str = str(response_key)
        response_key_str = response_key_str[2:30]
        print('resp key : '+response_key_str)
        response_key_entity = "Sec-WebSocket-Accept: " + response_key_str + "\r\n"
        clientSocket.send(bytes("HTTP/1.1 101 Web Socket Protocol Handshake\r\n", encoding="utf8"))
        clientSocket.send(bytes("Upgrade: websocket\r\n", encoding="utf8"))
        clientSocket.send(bytes(response_key_entity, encoding="utf8"))
        clientSocket.send(bytes("Connection: Upgrade\r\n\r\n", encoding="utf8"))
        print("send the hand shake data")


def parse_data(self, data):
    print('data: ' + str(data))
    v = data[1] & 0x7f
    if v == 0x7e:
        p = 4
    elif v == 0x7f:
        p = 10
    else:
        p = 2
    mask = data[p: p + 4]
    data = data[p + 4:]
    print(data)
    i = 0
    raw_str = ""
    for d in data:
        raw_str += chr(d ^ mask[i % 4])
        i += 1
    return raw_str


# 发送websocket server报文部分
def sendMessage(self, message):
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
    print(type(backMsgList[0]))
    for c in backMsgList:
        # if type(c) != bytes:
        # print(bytes(c, encoding="utf8"))
        message_byte += c
    message_byte += bytes(message, encoding="utf8")
    # print("message_str : ", str(message_byte))
    # print("message_byte : ", bytes(message_str, encoding="utf8"))
    # print(message_str[0], message_str[4:])
    # self.connection.send(bytes("0x810x010x63", encoding="utf8"))
    self.connection.send(message_byte)
