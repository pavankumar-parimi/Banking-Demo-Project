from pymongo import MongoClient


class ConnectionModel:

    db_name = "Bank"

    @staticmethod
    def connection(collection_name):
        """Returns the connection object which will help in creating the collections."""
        connection_object = MongoClient('localhost', 27017)

        return connection_object[ConnectionModel.db_name][collection_name]
