import pymongo
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


def getOne():
    OPTS = {
        'host': '192.168.3.181',
        "port": 27020,
        "dbname": 'turingchain',
        "connection_timeout": 5000,
        "max_tries": 3
    }
    return LocalMongoDBConnection(**OPTS, ssl=False)


conn = getOne()
sql = [
    {'$match': {'$and': [
        {'trans_details.inputs.owners_before': 'GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro'},
        {'trans_details.outputs.public_keys': 'GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro'}
    ]}},
    {'$unwind': '$trans_details'},
    {'$match': {'$and': [
        {'trans_details.inputs.owners_before': 'GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro'},
        {'trans_details.outputs.public_keys': 'GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro'},
        # {'trans_details.operation': 'CREATE'}
    ]}}, {'$sort': {'height': -1}},
    {'$limit': 1},
    {'$project': {'_id': 0}}

]
sql2 = [{"$match": {'time': {"$lte": 1558080604}}},
        {'$sort': {'_id': -1}},
        {'$limit': 1}
        ]
sql3 = [
    {'$sort': {'_id': -1}},
    {'$limit': 1}
]
s2 = [{'$match': {"app_hash": {"$regex": 's'}},

       },
      ]
res = conn.run(conn.collection('blocks').aggregate(sql, allowDiskUse=True))
# res = conn.run(conn.collection('b18435b902a1f06e37272e11e5f76abb81318306b7f6ca69402f2ed8185cc662').aggregate(sql3,
#                                                                                                              allowDiskUse=True))
assets = list(res)
print(assets)
# print(assets[0]['trans_details']['metadata']['user_selling_usd_rate'])
for k in res:
    print(k)

# ttime = assets[0]['block_header']['time']
# print(ttime)
