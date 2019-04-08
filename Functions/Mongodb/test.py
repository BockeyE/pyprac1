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


if __name__ == '__main__':
    OPTS = {
        'host': '192.168.3.183',
        "port": 27020,
        "dbname": '',
        "connection_timeout": 5000,
        "max_tries": 3
    }
    conn = LocalMongoDBConnection(**OPTS, ssl=False)
    sql = [
        {'$match': {'$or': [
            {'trans_details.asset.data.id': ''},
            {'trans_details.id': ''}
        ]}
        },
        {'$unwind': '$trans_details'},
        {'$match': {'$and': [{'$or': [{
            'trans_details.asset.data.id': ''},
            {'trans_details.id': ''}]},
            {'trans_details.operation': {'$ne': ''}}]}},
        {'$sort': {'height': -1}},
        {'$limit': 1}
    ]
    sql2 = [
        {'$match':
             {'trans_details.id': ''}
         },
        {'$unwind': '$trans_details'},
        {'$match': {'trans_details.id': ''}},

    ]
    sql3 = [
        {'$match':
            {'$or': [
                {'inputs.owners_before': ''},
                {'outputs.public_keys': ''}
            ]}
        }
    ]
    # res = conn.run(conn.collection('').aggregate(sql2, allowDiskUse=True))
    # res = conn.run(conn.collection('').find(sort=[('block_header.time', -1)], limit=10))
    res = conn.run(conn.collection('').aggregate(sql3, allowDiskUse=True))
    res1 = conn.run(conn.collection('transactions').find({'$and': [
        {'inputs.owners_before': 'GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro'},
        {'outputs.public_keys': {'$ne': 'GDAF71Hpr9jBpkbZvbh34kLVVUwCYjuzYw4yooJ6Jkro'}}]}
    )).count()
    print(res)
    for k in res:
        print(k)
