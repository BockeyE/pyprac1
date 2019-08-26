import time

from turingchaindb_driver import TuringchainDB

bdb_root_url = 'http://192.168.3.181:9984'
bdb = TuringchainDB(bdb_root_url)

# generate a keypair
from turingchaindb_driver.crypto import generate_keypair

# alice, bob = generate_keypair("rsa"), generate_keypair()
A_priv_key = "D6ahkZwKYx6D4zVgYpCXMcpRWjcirAu6hLuW4uLoGKoK"
A_pub_key = "GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro"
B_priv_key = "2pzwHj5tR7v7uxPH3L24R7X55FKpQdMakUw8wRyrEs6r"
B_pub_key = "21kZy9qAs8u4Lhvw7kcsEvccvmLW4rxo3UjNSK5s16i6"
# 部署智能合约
meta = ""
# with open('user_contract.py', 'r', encoding='UTF-8') as f:
with open('server_contract.py', 'r', encoding='UTF-8') as f:
    meta = f.read()
prepared_token_tx = bdb.transactions.prepare(
    operation='CONTRACT_UPDATE',
    signers=A_pub_key,
    recipients=[([A_pub_key], 10)],
    asset={"code": meta,"id": 'f5a95022e1cd6c9a1adf3c37dbfaa55c3a5d172578f2fc69dabb7483865e8efb'},
    metadata={"call": "deploy(100001)", 'tx_time': int(time.time())})
# fulfill and send the transaction
fulfilled_token_tx = bdb.transactions.fulfill(
    prepared_token_tx,
    private_keys=A_priv_key)
print(fulfilled_token_tx)

bdb.transactions.send_commit(fulfilled_token_tx)
print(fulfilled_token_tx['id'])

# print(fulfilled_token_tx)



