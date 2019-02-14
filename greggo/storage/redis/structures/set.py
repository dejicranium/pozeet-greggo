from greggo.config import REDIS_SERVER

class RedisSet:
    
    def __init__(self, key=None, redis=None, _max=6):
        self.redis = redis if redis else REDIS_SERVER
        self.key = key
        self.max = _max

    @classmethod
    def union(keys, *args):
        self.redis.sunion(keys, args)

    def set_key(self, key):
        #for class methods
        self.key = key


    def add(self, values): 
        if not isinstance(values, list): 
            values = [values]
        self.redis.sadd(self.key, *values)
        
    def count(self):
        return self.redis.scard(self.key)

    def _pop(self, count=1):
        return self.redis.spop(self.key, count)
    def get_all(self):
        return self.redis.smembers(self.key)

    def exists(self, member):
        return self.redis.sismember(self.key, member)

    def delete(self, member):
        return self.redis.srem(self.key, member)





    


if __name__ == '__main__':
    st = RedisSet('u_tl')
    st.add([1, 2, 4, 5])
    print(st.get_all('u_tl'))
