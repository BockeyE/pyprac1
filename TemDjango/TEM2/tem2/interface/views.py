# -*- coding:utf-8 -*-

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

BANK_PRIV_KEY = "499xiRSH5b49RCnSqNkgCYBdYb3exomfWPsDc8DLAXsB"
BANK_PUB_KEY = "H9wRpUwYxMzXz4EZqh3WfESUKTgtWC84w7V3XTCcHaYd"


print("views =========")


status_code = 200
err_code = 500


@api_view(['POST'])
def handle_tx(request):
    # data = request.data
    # print(data)
    # prepared_token_tx = bdb.transactions.prepare(
    #     operation='CONTRACT_EXECUTE',
    #     signers=A_pub_key,
    #     recipients=[([A_pub_key], 10)],
    #     # asset={"id": fulfilled_token_tx['id']},
    #     # asset={"id": "35b94760bc18b394fef46639e63b8d76f5f5e11943c18460b44c7f32792b820d"},
    #     asset={"id": "8fd262e48cf4934494725a5a40527bc51da74a533c0083c17990309bf4775600"},
    #     metadata={"call": "cross_transfer(\"test\",1002)"})

    if not 1:
        return None
    # priv_key = cryptoutils().decrypt(text_as_key=(company + code), keystore=keystore)
    return Response(data="priv")


@api_view(['GET'])
def test(request, format=None):
    key = 'test'
    if not key:
        returndata = 'The parameter is empty'
    else:
        pub, priv, token = ""
        returndata = {
            'pub': pub,
            'priv': priv,
            'token': token
        }
    return Response(data=returndata)


def empty_req_info():
    returndata = 'please don\'t send empty info'
    return Response(data=returndata, status=err_code)


def except_ret_info(s):
    returndata = 'please check your input, refresh page and retry, exception info : ' + s
    return Response(data=returndata, status=err_code)
