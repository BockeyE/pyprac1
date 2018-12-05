import hashlib
from Crypto.Cipher import AES
from rest_framework.decorators import api_view
from rest_framework.response import Response
from binascii import b2a_hex, a2b_hex

@api_view(['GET'])
def test(request, format=None):
    print('==============>get_public_key')
    returndata = ''
    key = 'test'
    if key == None:
        returndata = 'The parameter is empty'
    else:
        returndata = "publickey"
        return Response(returndata)


# zdz creat publickey and privatekey
@api_view(['GET'])
def get_public_key(request, key, format=None):
    private_key, public_key = crypto.generate_key_pair();

    save_priv = private_key + ('\0' * 4)
    save_pub = public_key + ('\0' * 4)
    m = hashlib.md5(key.encode('utf-8')).hexdigest()

    print('==============>' + public_key)

    # aes = AES.new(m, AES.MODE_CBC)  # 初始化加密器
    #
    encrypted_text = encryptos(key=m, text=save_priv)

    text_decrypted = decrypt(key=m, text=encrypted_text)

    returndata = {'private_key': private_key, 'public_key': public_key,
                  'key': key, 'MD5': m, 'other things': 'other things',
                  '================': '============',
                  'encoded: ': encrypted_text,
                  'decrypted_text': text_decrypted

                  }
    return Response(returndata)


def encryptos(key, text):
    print(key)
    print('===========================================')
    cryptors = AES.new(key.encode('utf-8'), AES.MODE_CBC, b'1231234564567777')
    encodetext = cryptors.encrypt(text.encode('utf-8'))

    return b2a_hex(encodetext);


def decrypt(key, text):
    cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, b'1231234564567777')
    plain_text = cryptor.decrypt(a2b_hex(text))
    # return plain_text.rstrip('\0')
    return bytes.decode(plain_text).rstrip('\0')
