from greggo.config import REDIS_SERVER

class RedisSortedSet:
    def __init__(self, key, redis=None, _max=2):
        self.key = key
        self.max = _max
        self.redis = redis or REDIS_SERVER


    def add(self, members):
        if not isinstance(members, list):
            members = [members]
            
        self.redis.zadd(self.key, *members)
        
        count = self.count()
        #if count < self.max:
        #    all_members = self.get_all()
       #     members_to_remove = all_members[self.max+1:]
        #    self.remove(members_to_remove)


    def remove(self, members):
        if not isinstance(members, list):
            members = [members]
        self.redis.zrem(self.key, *members)

    def count(self):
        return self.redis.zcard(self.key)

    def get_score(self, member):
        return self.redis.zscore(self.key, member)

    def get_all(self, start=None, end=None):
        start = start or 0
        end = end or self.count() - 1
        return self.redis.zrange(self.key, start, end)
    
if __name__ == '__main__':
    tren = RedisSortedSet('tr_o')
    print("starting")
    for i in range(0, 1000):
        print(tren.remove(i))
    
    tren = RedisSortedSet('tr_p')
    print("starting")
    for i in range(0, 1000):
        print(tren.remove(i))

    tren = RedisSortedSet('tr_c')
    print("starting")
    for i in range(0, 1000):
        print(tren.remove(i))