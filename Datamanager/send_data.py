import pymongo


class MongoDBConnection:
    _instance = None

    @classmethod
    def get_instance(cls, connection_string):
        if cls._instance is None:
            cls._instance = cls(connection_string)
        return cls._instance

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.client = None

    def connect(self):
        if self.client is None:
            self.client = pymongo.MongoClient(self.connection_string)

    def get_database(self, db_name):
        self.connect()
        return self.client[db_name]

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
