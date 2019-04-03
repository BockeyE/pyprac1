# -*- coding:utf-8 -*-
# import base64
# s = b"12345678"
# print(base64.b64encode(s))

content = """
# -*- coding:utf-8 -*-
import pymongo
MONGO_OPTS = {
    'socketTimeoutMS': 20000,
}
class Lazy:
    def __init__(self):
        self.stack = []

    def __getattr__(self, name):
        self.stack.append(name)
        return self

    def __call__(self, *args, **kwargs):
        self.stack.append((args, kwargs))
        return self

    def __getitem__(self, key):
        self.stack.append('__getitem__')
        self.stack.append(([key], {}))
        return self

    def run(self, instance):
        last = instance

        for item in self.stack:
            if isinstance(item, str):
                last = getattr(last, item)
            else:
                last = last(*item[0], **item[1])

        self.stack = []
        return last

class Connection:
    def __init__(self, host=None, port=None, dbname=None,
                 connection_timeout=None, max_tries=None,
                 **kwargs):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.connection_timeout = connection_timeout
        self.max_tries = max_tries
        self.max_tries_counter = range(self.max_tries)
        self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            self.connect()
        return self._conn

    def run(self, query):
        raise NotImplementedError()

    def connect(self):
        attempt = 0
        for i in self.max_tries_counter:
            attempt += 1
            try:
                self._conn = self._connect()
            except ConnectionError as exc:
                print('Attempt %s/%s. Connection to %s:%s failed after %sms.',
                               attempt, self.max_tries if self.max_tries != 0 else '∞',
                               self.host, self.port, self.connection_timeout)
                if attempt == self.max_tries:
                    print('Cannot connect to the Database. Giving up.')
                    raise ConnectionError() from exc
            else:
                break

class LocalMongoDBConnection(Connection):
    def __init__(self, replicaset=None, ssl=None, login=None, password=None,
                 ca_cert=None, certfile=None, keyfile=None,
                 keyfile_passphrase=None, crlfile=None, **kwargs):
        super().__init__(**kwargs)
        self.replicaset = replicaset
        self.ssl = ssl
        self.login = login
        self.password = password
        self.ca_cert = ca_cert
        self.certfile = certfile
        self.keyfile = keyfile
        self.keyfile_passphrase = keyfile_passphrase
        self.crlfile = crlfile

    @property
    def db(self):
        return self.conn[self.dbname]

    def query(self):
        return Lazy()

    def collection(self, name):
        return self.query()[self.dbname][name]

    def run(self, query):
        try:
            try:
                return query.run(self.conn)
            except pymongo.errors.AutoReconnect as exc:
                print('Lost connection to the database, '
                               'retrying query.')
                return query.run(self.conn)
        except pymongo.errors.AutoReconnect as exc:
            print(f'DETAILS: {exc.details}')
        except pymongo.errors.DuplicateKeyError as exc:
            print(f'DETAILS: {exc.details}')
        except pymongo.errors.OperationFailure as exc:
            print(f'DETAILS: {exc.details}')

    def _connect(self):
        try:
            if self.ca_cert is None or self.certfile is None or \
                    self.keyfile is None or self.crlfile is None:
                client = pymongo.MongoClient(self.host,
                                             self.port,
                                             replicaset=self.replicaset,
                                             serverselectiontimeoutms=self.connection_timeout,
                                             ssl=self.ssl,
                                             **MONGO_OPTS)
                if self.login is not None and self.password is not None:
                    client[self.dbname].authenticate(self.login, self.password)
            else:
                print('Connecting to MongoDB over TLS/SSL...')
                client = pymongo.MongoClient(self.host,
                                             self.port,
                                             replicaset=self.replicaset,
                                             serverselectiontimeoutms=self.connection_timeout,
                                             ssl=self.ssl,
                                             ssl_ca_certs=self.ca_cert,
                                             ssl_certfile=self.certfile,
                                             ssl_keyfile=self.keyfile,
                                             ssl_pem_passphrase=self.keyfile_passphrase,
                                             ssl_crlfile=self.crlfile,
                                             ssl_cert_reqs=CERT_REQUIRED,
                                             **MONGO_OPTS)
                if self.login is not None:
                    client[self.dbname].authenticate(self.login,
                                                     mechanism='MONGODB-X509')

            return client

        except (pymongo.errors.ConnectionFailure,
                pymongo.errors.OperationFailure) as exc:
            print(f'DETAILS: {exc.details}')
        except pymongo.errors.ConfigurationError as exc:
            print(f'DETAILS: {exc.details}')

class Contract(object):
    CONNECTION = "b4ac114607ec673d8baf85faf603ad28147be68bd5ed6c79ed5f8b50cc79482c"  # 执行合约时CONNECTION动态替换成部署合约的txid，SENDER_PUBKEY动态替换成合约调用方的公钥
    SENDER_PUBKEY = "GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro"  # 对于查询动作，SENDER_PUBKEY = "QUERY"
    HOST = "127.0.0.1"
    PORT = 27017
    LOGIN = None
    PASSWORD = None
    DATABASE = "bigchain"
    CONNECTION_TIMEOUT = 5000
    MAX_RETRIES = 3

    def __init__(self):
        OPTS = {
            'host': self.HOST,
            "port": self.PORT,
            "dbname": self.DATABASE,
            "connection_timeout": self.CONNECTION_TIMEOUT,
            "max_tries": self.MAX_RETRIES
        }
        self.conn = LocalMongoDBConnection(**OPTS, login=self.LOGIN, password=self.PASSWORD, ssl=False)

    # sql = [
    #     {'$match': {'$and': [{'asset_id': tokenid},
    #                          {'public_keys': account_from}]}},
    #     {'$unwind': '$public_keys'},
    #     {'$match': {'$and': [{'asset_id': tokenid},
    #                          {'public_keys': account_from}]}}
    # ]
    def mongo_aggregate(self, sql):
        return self.conn.run(self.conn.collection(self.CONNECTION).aggregate(sql, allowDiskUse=True))

    # sql = {'height': block_id}
    def mongo_find_one(self, sql):
        return self.conn.run(
            self.conn.collection(self.CONNECTION)
                .find_one(sql))

    # sql = {'height': height}
    def mongo_replace_one(self, sql, data):
        if self.SENDER_PUBKEY == "QUERY":  # 对于查询操作，写入方法失效
            return None
        return self.conn.run(
            self.conn.collection(self.CONNECTION).replace_one(
                sql,
                data,
                upsert=True
            )
        )

class Token(Contract):
    def __init__(self):
        super().__init__()
        return
        
    def deploy(self, amount):  # 初始化，合约部署时调用，owner设置将无法更改
        owner = self.mongo_find_one({"key": "owner"})
        if owner == None:
            self.mongo_replace_one({"key": "owner"}, {"key": "owner", "value": self.SENDER_PUBKEY})
            self.mongo_replace_one({"key": self.SENDER_PUBKEY}, {"key": self.SENDER_PUBKEY, "value": amount})
        return

    def balanceOf(self, owner):
        query = self.mongo_find_one({"key": owner})
        if query:
            return query["value"]
        return 0

    def transfer(self, to, value):
        balance_from = 0
        query = self.mongo_find_one({"key": self.SENDER_PUBKEY})
        if query:
            balance_from = query["value"]
        if balance_from < value:
            return False
        query = self.mongo_find_one({"key": to})
        balance_to = 0
        if query:
            balance_to = query["value"]
        self.mongo_replace_one({"key": self.SENDER_PUBKEY}, {"key": self.SENDER_PUBKEY, "value": balance_from - value})
        self.mongo_replace_one({"key": to}, {"key": to, "value": balance_to + value})
        return True

def main():
    contractobject = Token()
    print("sdfsdfsdf")
    return contractobject.transfer("1231335500000", 1)
"""

import time
vars = {}
print(1)
a = time.time()
code = compile(content, '<string>', 'exec')
print(2)
exec(content, vars, vars)
print(3)
output = vars['main']()
print("output", output)
print(time.time() - a)
