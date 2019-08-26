# coding=utf8

import pymongo


class Con(object):

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://127.0.0.1:27017/baas')['baas']
        self.collection = self.client['user']

    def count_all(self):
        print(type(self.client))
        print(type(self.collection))
        ret = self.collection.count({})
        return ret


if __name__ == '__main__':
    print(Con().count_all())
