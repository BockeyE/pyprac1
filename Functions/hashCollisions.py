import hashlib

a = bytearray.fromhex(
    '0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c'
    '00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef')
b = bytearray.fromhex(
    '0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c'
    '00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef')
c = bytearray.fromhex(
    '0e306561559aa787d00bc6f70bbdfe3404cf03659e784f8534c'
    '00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef')

#    ----------------------------------------704/744----------------------------------------------------------------------------------
print(hashlib.md5(a).hexdigest())

print(hashlib.md5(b).hexdigest())
print(hashlib.md5(c).hexdigest())
ma = hashlib.md5(a).hexdigest()
mb = hashlib.md5(b).hexdigest()
print((' md5-a compared with md5-b :  ') + str(ma == mb))
