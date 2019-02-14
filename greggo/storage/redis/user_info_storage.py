from greggo.storage.redis.structures.hash import RedisHash
from greggo.config import REDIS_SERVER
import redis as r




class UserInfoStorage:
    #the data structure used is a redis' hash\
    key_format = 'user:%(user_id)s'

    def __init__(self, redis=REDIS_SERVER):
        self.redis = redis or r.Redis()
        self.redis_hash = RedisHash(self.redis)

    def create_user(self, _id, user_details): #r_server = redis server
        storage = self.redis_hash
        key = self.key_format % {'user_id': str(_id)}
        status = storage.set(key, user_details)
        return status

    def get_user_detail(self, _id, detail):
        storage = self.redis_hash
        key = self.key_format % {'user_id': str(_id)}
        return storage.get(key, detail)

    def get_user_details(self, _id):
        storage = self.redis_hash
        key = self.key_format % {'user_id': str(_id)}
        return storage.get_all(key)


if __name__ == '__main__':
    storage = UserInfoStorage()
    print(storage.get_user_detail(11000, 'v'))
