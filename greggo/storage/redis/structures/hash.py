from greggo.config import REDIS_SERVER

class RedisHash():
    def __init__(self, redis_server):
        self.redis = redis_server

    def set(self, key, field):
        return self.redis.hmset(key, field)

    def get(self, key, field):
        return self.redis.hget(key, field) 
        
    def increment(self, key, field, amount=1):
        return self.redis.hincrby(key, field, amount)

    def get_all(self, key):
        return self.redis.hgetall(key)

    def delete(self, key, items):
        return self.redis.hdel(key, items)



if __name__ == '__main__':
    r = RedisHash(REDIS_SERVER)

    for i in range(0, 20):
        for z in range(0, 50): 
            print(r.delete('pv_a_s:{}'.format(z), 'None::{}'.format(i)))

    print(r.get_all('pv_a_s:1'))

    