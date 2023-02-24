from pymongo import MongoClient
from datetime import date, datetime


class MongoDBConnection():
    def __init__(self, username, password, hostname, port=27017):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.client = None

    def __enter__(self):
        CONNECTION_STRING = f"mongodb://{self.username}:{self.password}@{self.hostname}:{self.port}"
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client['test']
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


if __name__ == '__main__':
    current_date = date.today().strftime("%m/%d/%y")
    current_time = datetime.now().strftime("%H:%M:%S")
    with MongoDBConnection('admin', 'admin', 'localhost') as db:
        collection = db['alarm_status']
        collection.insert_one({"Date": current_date, "Time": current_time, "Point": "swap-memory",
                               "Status": "Exceeding the critical operating mark"}
                              )
