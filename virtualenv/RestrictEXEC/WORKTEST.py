

import pymongo
from copy import deepcopy
import re
from ssl import CERT_REQUIRED

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
            if self.ca_cert is None or self.certfile is None or self.keyfile is None or self.crlfile is None:
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
    __connection = "0295ccf1d8ee0c8f207ed19d6eed723e0db90dc76c26bbcb0e90a54cf9536dd7"  # 执行合约时CONNECTION动态替换成部署合约的txid，SENDER_PUBKEY动态替换成合约调用方的公钥
    SENDER_PUBKEY = "GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro"  # 对于查询动作，SENDER_PUBKEY = "QUERY"
    __host = "localhost"
    __port = 27017
    __login = None
    __password = None
    __dbname = "turingchain"
    __connection_timeout = 5000
    __max_retries = 3

    def __init__(self):
        OPTS = {
            'host': self.__host,
            "port": self.__port,
            "dbname": self.__dbname,
            "connection_timeout": self.__connection_timeout,
            "max_tries": self.__max_retries
        }
        self.__conn = LocalMongoDBConnection(**OPTS, login=self.__login, password=self.__password, ssl=False)

    def mongo_aggregate(self, sql):
        return self.__conn.run(self.__conn.collection(self.__connection).aggregate(sql, allowDiskUse=True))

    def mongo_find_one(self, sql):
        return self.__conn.run(
            self.__conn.collection(self.__connection)
                .find_one(sql))

    def mongo_replace_one(self, sql, data):
        if self.SENDER_PUBKEY == "QUERY":  # 对于查询操作，写入方法失效
            return None
        return self.__conn.run(
            self.__conn.collection(self.__connection).replace_one(
                sql,
                data,
                upsert=True
            )
        )

    def cross_contract_call(self, contract_address, callfuncstr):
        contract_header = '''
import pymongo
from copy import deepcopy
import re
from ssl import CERT_REQUIRED
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
            if self.ca_cert is None or self.certfile is None or self.keyfile is None or self.crlfile is None:
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
    __connection = "_TURING_CONTRACT_TXID"  # 执行合约时CONNECTION动态替换成部署合约的txid，SENDER_PUBKEY动态替换成合约调用方的公钥
    SENDER_PUBKEY = "_TURING_CONTRACT_OWNER_BEFORE"  # 对于查询动作，SENDER_PUBKEY = "QUERY"
    __host = "_HOST"
    __port = _PORT
    __login = _LOGIN
    __password = _PASSWORD
    __dbname = "_DBNAME"
    __connection_timeout = _CONNECTION_TIMEOUT
    __max_retries = _MAX_RETRIES

    def __init__(self):
        OPTS = {
            'host': self.__host,
            "port": self.__port,
            "dbname": self.__dbname,
            "connection_timeout": self.__connection_timeout,
            "max_tries": self.__max_retries
        }
        self.__conn = LocalMongoDBConnection(**OPTS, login=self.__login, password=self.__password, ssl=False)

    def mongo_aggregate(self, sql):
        return self.__conn.run(self.__conn.collection(self.__connection).aggregate(sql, allowDiskUse=True))

    def mongo_find_one(self, sql):
        return self.__conn.run(
            self.__conn.collection(self.__connection)
                .find_one(sql))

    def mongo_replace_one(self, sql, data):
        if self.SENDER_PUBKEY == "QUERY":  # 对于查询操作，写入方法失效
            return None
        return self.__conn.run(
            self.__conn.collection(self.__connection).replace_one(
                sql,
                data,
                upsert=True
            )
        )
'''
        contract_footer = '''
def main():
    contractobject = _CONTRACT_CLASS_NAME()
    return contractobject._CONTRACT_FUNCTION
'''
        contract_cross_code_template = '''

    def cross_contract_call(self, contract_address, callfuncstr):
        contract_header = \'\'\'
import pymongo
from copy import deepcopy
import re
from ssl import CERT_REQUIRED
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
            if self.ca_cert is None or self.certfile is None or self.keyfile is None or self.crlfile is None:
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
    __connection = "_TURING_CONTRACT_TXID"  # 执行合约时CONNECTION动态替换成部署合约的txid，SENDER_PUBKEY动态替换成合约调用方的公钥
    SENDER_PUBKEY = "_TURING_CONTRACT_OWNER_BEFORE"  # 对于查询动作，SENDER_PUBKEY = "QUERY"
    __host = "_HOST"
    __port = _PORT
    __login = _LOGIN
    __password = _PASSWORD
    __dbname = "_DBNAME"
    __connection_timeout = _CONNECTION_TIMEOUT
    __max_retries = _MAX_RETRIES

    def __init__(self):
        OPTS = {
            'host': self.__host,
            "port": self.__port,
            "dbname": self.__dbname,
            "connection_timeout": self.__connection_timeout,
            "max_tries": self.__max_retries
        }
        self.__conn = LocalMongoDBConnection(**OPTS, login=self.__login, password=self.__password, ssl=False)

    def mongo_aggregate(self, sql):
        return self.__conn.run(self.__conn.collection(self.__connection).aggregate(sql, allowDiskUse=True))

    def mongo_find_one(self, sql):
        return self.__conn.run(
            self.__conn.collection(self.__connection)
                .find_one(sql))

    def mongo_replace_one(self, sql, data):
        if self.SENDER_PUBKEY == "QUERY":  # 对于查询操作，写入方法失效
            return None
        return self.__conn.run(
            self.__conn.collection(self.__connection).replace_one(
                sql,
                data,
                upsert=True
            )
        )
\'\'\'
        contract_footer = \'\'\'
def main():
    contractobject = _CONTRACT_CLASS_NAME()
    return contractobject._CONTRACT_FUNCTION
\'\'\'
        contract_cross_code_template = \'\'\'
_CROSS_CONTRACT_CODE
\'\'\'
        def gen_contract_cross_code(contract_cross_code_template):
            code = deepcopy(contract_cross_code_template)
            replace_code = code.replace("\\\\", "\\\\\\\\")
            replace_code = replace_code.replace("\'\'\'", "\\\\'\\\\'\\\\'")
            code = code.replace("_CROSS_CONTRACT_CODE", replace_code, 1)
            return code

        contract_cross_code = gen_contract_cross_code(contract_cross_code_template)

        contract = contract_header
        contract = contract.replace("_TURING_CONTRACT_TXID", contract_address)
        contract = contract.replace("_TURING_CONTRACT_OWNER_BEFORE", "QUERY" if self.SENDER_PUBKEY is "QUERY" else self.__connection)
        contract = contract.replace("_HOST", self.__host)
        contract = contract.replace("_PORT", str(self.__port))
        contract = contract.replace("_LOGIN", self.__login if self.__login is not None else "None")
        contract = contract.replace("_PASSWORD",  self.__password if self.__password is not None else "None")
        contract = contract.replace("_DBNAME", self.__dbname)
        contract = contract.replace("_CONNECTION_TIMEOUT", str(self.__connection_timeout))
        contract = contract.replace("_MAX_RETRIES", str(self.__max_retries))

        sql = [
            {'$match': {'$or': [
                {'trans_details.asset.data.id': contract_address},
                {'trans_details.id': contract_address}
            ]}},
            {'$unwind': '$trans_details'},
            {'$match': {'$and': [{'$or': [{
                'trans_details.asset.data.id': contract_address},
                {'trans_details.id': contract_address}]},
                {'trans_details.operation': {'$ne': 'CONTRACT_EXECUTE'}}]}},
            {'$sort': {'height': -1}},
            {'$limit': 1}
        ]

        blocks = self.__conn.run(self.__conn.collection("blocks").aggregate(sql, allowDiskUse=True))
        assets = list(blocks)
        if len(assets) != 0:
            assets = assets[0]['trans_details']['asset']
            # contract = contract + assets["data"]["code"] + contract_footer
            key_word = re.search("class \\s*(\\w*)\\W*Contract\\s*", assets["data"]["code"])
            if key_word:
                classname = key_word.group(1)
                contract_footer = contract_footer.replace("_CONTRACT_CLASS_NAME", classname)
                contract_footer = contract_footer.replace("_CONTRACT_FUNCTION", callfuncstr)
                contract = contract + contract_cross_code + assets["data"]["code"] + contract_footer
                # fo = open("/home/output" + contract_address + ".py", "w")
                # fo.write(contract)
                output = ""
                try:
                    vars = {}
                    compile(contract, '<string>', 'exec')
                    exec (contract, vars, vars)
                    temp = vars['main']()
                    output = "%s" % temp
                    print("ContractExecute_ok_output===>", output)
                except Exception as e:
                    output = "Failed to execute smart contract, Error message:" + str(
                        e.__class__.__name__) + ' ' + str(e)
                    print("ContractExecute_error_output===>", output)
                finally:
                    return {"tx_id": contract_address, "result": output}
        else:
            return {"tx_id": contract_address, "result": "Address '{}' no smart contract".format(contract_address)}

'''

        def gen_contract_cross_code(contract_cross_code_template):
            code = deepcopy(contract_cross_code_template)
            replace_code = code.replace("\\", "\\\\")
            replace_code = replace_code.replace("'''", "\\'\\'\\'")
            code = code.replace("_CROSS_CONTRACT_CODE", replace_code, 1)
            return code

        contract_cross_code = gen_contract_cross_code(contract_cross_code_template)

        contract = contract_header
        contract = contract.replace("_TURING_CONTRACT_TXID", contract_address)
        contract = contract.replace("_TURING_CONTRACT_OWNER_BEFORE",
                                    "QUERY" if self.SENDER_PUBKEY is "QUERY" else self.__connection)
        contract = contract.replace("_HOST", self.__host)
        contract = contract.replace("_PORT", str(self.__port))
        contract = contract.replace("_LOGIN", self.__login if self.__login is not None else "None")
        contract = contract.replace("_PASSWORD", self.__password if self.__password is not None else "None")
        contract = contract.replace("_DBNAME", self.__dbname)
        contract = contract.replace("_CONNECTION_TIMEOUT", str(self.__connection_timeout))
        contract = contract.replace("_MAX_RETRIES", str(self.__max_retries))

        sql = [
            {'$match': {'$or': [
                {'trans_details.asset.data.id': contract_address},
                {'trans_details.id': contract_address}
            ]}},
            {'$unwind': '$trans_details'},
            {'$match': {'$and': [{'$or': [{
                'trans_details.asset.data.id': contract_address},
                {'trans_details.id': contract_address}]},
                {'trans_details.operation': {'$ne': 'CONTRACT_EXECUTE'}}]}},
            {'$sort': {'height': -1}},
            {'$limit': 1}
        ]

        blocks = self.__conn.run(self.__conn.collection("blocks").aggregate(sql, allowDiskUse=True))
        assets = list(blocks)
        if len(assets) != 0:
            assets = assets[0]['trans_details']['asset']
            # contract = contract + assets["data"]["code"] + contract_footer
            key_word = re.search("class \s*(\w*)\W*Contract\s*", assets["data"]["code"])
            if key_word:
                classname = key_word.group(1)
                contract_footer = contract_footer.replace("_CONTRACT_CLASS_NAME", classname)
                contract_footer = contract_footer.replace("_CONTRACT_FUNCTION", callfuncstr)
                contract = contract + contract_cross_code + assets["data"]["code"] + contract_footer
                # fo = open("/home/output" + contract_address + ".py", "w")
                # fo.write(contract)
                output = ""
                try:
                    vars = {}
                    compile(contract, '<string>', 'exec')
                    exec(contract, vars, vars)
                    temp = vars['main']()
                    output = "%s" % temp
                    print("ContractExecute_ok_output===>", output)
                except Exception as e:
                    output = "Failed to execute smart contract, Error message:" + str(
                        e.__class__.__name__) + ' ' + str(e)
                    print("ContractExecute_error_output===>", output)
                finally:
                    return {"tx_id": contract_address, "result": output}
        else:
            return {"tx_id": contract_address, "result": "Address '{}' no smart contract".format(contract_address)}


# contract_req_cross
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

    def cross_transfer(self, to, value):
        self.transfer(to, value)
        return self.cross_contract_call("TXXXXX", "cross_transfer('" + to + "',100)")


def main():
    contractobject = Token()
    return contractobject.cross_transfer("test", 1001)
