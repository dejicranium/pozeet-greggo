from greggo.config import REDIS_SERVER

"""
@NOTE: I have not tested method: 'push_if_key'

I need to read about redis pipeline too
"""


class RedisList:

    def __init__(self, key=None, redis_server=None):
        self.redis = redis_server or REDIS_SERVER
        self.key = key

    #this is needed for classmethods
    #check timeline_storage for add_to_many_categories
    def set_key(self, key):
        self.key = key


    def get_length(self):
        return self.redis.llen(self.key)


    def trim(self, start, end):
        return self.redis.ltrim(self.key, start, end)


    def pop_last(self):
        return self.redis.rpop(self.key)


    def push(self, values, where=None,):
        if not isinstance(values, list):
            values = [values]
        if where == 'tail':
            return self.redis.rpush(self.key, *values)
        else:
            return self.redis.lpush(self.key, *values)


    def push_if_key(self, key, value, where=None):
        if where == 'tail':
            return self.redis.rpushx(self.key, value)
        else:
            return self.redis.lpushx(self.key, value)


    def pop_first(self, key):
        return self.redis.lpop(self.key)


    def get_items(self, start, end):
        return self.redis.lrange(self.key, start, end)


if __name__ == '__main__':
    storage = RedisList(REDIS_SERVER)

    storage.push('feed:user:1', [3212, 323, 2123, 3, 45, 34, 46, 54])
    length = storage.get_length('feed:user:1')
    storage.pop_first('feed:user:1')
    
    print(storage.get_items('feed:user:1', 0, 3))
