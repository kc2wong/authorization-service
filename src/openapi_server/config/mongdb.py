from pymongo import MongoClient
from dotenv import dotenv_values

mongoClient = None

def get_database():

    global mongoClient
    if mongoClient is None:        
        config = dotenv_values(".env")

        uri = config["MONGODB_URI"]
        idx = uri.index("://")
        protocol = uri[0:idx]
        host = uri[idx+3:]

        connect_string = "{0}://{1}:{2}@{3}".format(protocol, config["MONGODB_USER"], config["MONGODB_PASSWORD"], host)
        mongoClient = MongoClient(connect_string)

    return mongoClient["authorization-db"]