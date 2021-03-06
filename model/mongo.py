from pymongo import MongoClient
from os import getenv


class Movies():

    def __init__(self):
        client = MongoClient(getenv('MONGO_SERVER'), int(getenv('MONGO_PORT')))
        db = client[getenv('MONGO_DB')]
        db.authenticate(getenv('MONGO_USER'), getenv('MONGO_PASS'))
        self.movies = db.movies
        d = self.movies.find_one(sort=[('_id', -1)])
        if d is None:
            self.id = 0
        else:
            self.id = int(d['id'])

    def create_movie(self, data):
        self.id += 1
        data['id'] = str(self.id)
        self.movies.insert_one(data)
        return self.movies.find_one(data, projection={'_id': False})

    def get_movie(self, id):
        return self.movies.find_one({'id': str(id)}, projection={'_id': False})

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'id': str(id)}, data)

    def delete_movie(self, id):
        return self.movies.find_one_and_delete({'id': str(id)}, projection={'_id': False})


class Series:
    def __init__(self):
        client = MongoClient(getenv('MONGO_SERVER'), int(getenv('MONGO_PORT')))
        db = client[getenv('MONGO_DB')]
        db.authenticate(getenv('MONGO_USER'), getenv('MONGO_PASS'))
        self.series = db.series
        d = self.series.find_one(sort=[('_id', -1)])
        if d is None:
            self.id = 0
        else:
            self.id = int(d['id'])

    def create_series(self, data):
        self.id += 1
        data['id'] = str(self.id)
        self.series.insert_one(data)
        return self.series.find_one(data, projection={'_id': False})

    def get_series(self, id):
        return self.series.find_one({'id': str(id)}, projection={'_id': False})

    def get_all_series(self):
        s = {}
        for i in self.series.find(projection={'_id': False}):
            s[i['id']] = i
        return s

    def update_series(self, id, data):
        s = self.series.find_one({'id': str(id)}, projection={'_id': False})
        for k, v in data.items():
            s[k] = v
        return self.series.find_one_and_replace({'id': str(id)}, s, projection={'_id': False})

    def delete_series(self, id):
        return self.series.find_one_and_delete({'id': str(id)}, projection={'_id': False})

    def delete_all_series(self):
        self.series.delete_many({})
        return self.get_all_series()


class Users:
    def __init__(self):
        client = MongoClient(getenv('MONGO_SERVER'), int(getenv('MONGO_PORT')))
        db = client[getenv('MONGO_DB')]
        db.authenticate(getenv('MONGO_USER'), getenv('MONGO_PASS'))
        self.users = db.users

    def create_user(self, data):
        if self.get_user(data['username']):
            return False
        self.users.insert_one(data)
        return True

    def get_user(self, username):
        return self.users.find_one({'username': username}, projection={'_id': False})


class Health:
    def check_connection(self):
        try:
            client = MongoClient(getenv('MONGO_SERVER'), int(getenv('MONGO_PORT')))
            db = client[getenv('MONGO_DB')]
            db.authenticate(getenv('MONGO_USER'), getenv('MONGO_PASS'))
        except:
            return False
        return True