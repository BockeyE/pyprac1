import pymongo


class LocalData:

    def __init__(self, host, port, dbname):
        # self.client = pymongo.MongoClient('mongodb://%s:%s@%s:%d/%s' % (settings.
        #                                                                 MONGO_USER, settings.MONGO_PWD,
        #                                                                 host, port,
        #                                                                 settings.
        #                                                            MONGO_AUTHDB))[dbname]
        self.client = pymongo.MongoClient(host, port,
                                          socketTimeoutMS=20000)[dbname]
        self.collection = self.client['test_data']


if __name__ == '__main__':
    LocalData('47.100.39.147', 9017, 'lilytest').collection.insert({'time': '2018', 'time2': '2019'})
