# import pymongo

MONGO_OPTS = {
    'socketTimeoutMS': 20000,
}


def main():

    return pymongo.MongoClient("127.0.0.1",27017)
