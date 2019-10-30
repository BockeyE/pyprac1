import base64
import hashlib

f = open("C:\ZZBK\sqs.pdf", 'rb', True)
data=f.read()
f.close()
print(":::::")
# print(data)
sha256obj = hashlib.sha256()

# sha256obj.update(base64.b64encode(data))
sha256obj.update((data))

hash_value = sha256obj.hexdigest()
# sha256obj.update("AAA".encode("UTF-8"))


# print(CalcFileSha256())
# 61e36ec48758e547b81d2434670a57e0
# c9b02e9478ee7a210ae0c89ae72899ab


print(hash_value)
