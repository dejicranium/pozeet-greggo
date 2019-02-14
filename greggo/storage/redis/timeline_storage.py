from greggo.config import REDIS_SERVER
from greggo.storage.redis.structures.list import RedisList
from greggo.storage.redis.structures.set import RedisSet
from greggo.storage.redis.structures.sorted_set import RedisSortedSet

class BaseRedisTimelineStorage:
    def __init__(self, key, redis=None):
        self.redis = redis or REDIS_SERVER
        self.key = key
        self.storage = RedisSet

    def get_key(self):
        return self.key

    #useful when iterating
    def change_key(self, key):
        self.key = key

    def get_storage(self):
        key = self.get_key()
        redis = self.redis
        return self.storage(key, redis)

    def add(self):
        raise NotImplementedError("You need to implement this")

    def get(self):
        raise NotImplementedError("You need to implement this")


class RedisUserTimelineStorage(BaseRedisTimelineStorage):
    
    def __init__(self, key, redis=None):
        self.key = key
        self.redis = redis
        super().__init__(self.key, self.redis)

    def add_many(self, values):
        storage = self.get_storage()
        storage.add(values)

    def get_many(self, start=None, end=None): 
        storage = self.get_storage()
        return storage.get_all()

    def remove_many(self, members):
        storage = self.get_storage()
        storage.delete(members)


class RedisCategoryTimelineStorage(BaseRedisTimelineStorage):
    """
    This stores the denormalized data of category activities
    """

    key_format = 'c_tl:%(category_id)s'

    def __init__(self, category_id):
        self.key = self.key_format % {'category_id' : category_id}
        super().__init__(self.key)


    @classmethod
    def add_to_many(cls, categories_id, activity_id):
        store = RedisSet()
        for i in range(0, len(categories_id)):
            key = cls.key_format % {'category_id': categories_id[i]}
            store.set_key(key)
            store.add(activity_id)
    
    @classmethod
    def get_activities_from_categories(cls, categories_id):
        store = RedisSet()
        activities = []
        for i in range(0, len(categories_id)):
            key = cls.key_format % {'category_id': categories_id[i]}
            store.set_key(key)
            items = store.get_items(0, length)
            items = [int(item.decode('utf-8')) for item in items]
            activities.append(items)

        return activities

    def add(self, activity_id):
        store = self.get_storage()
        key = self.get_key()
        store.push(activity_id)

    def count(self):
        store = self.get_storage()
        return store.get_length()

    def get_feed(self):
        store = self.get_storage()
        activities = store.get_all()
        activities = [int(activity.decode('utf-8')) for activity in activities]
        return activities


class RedisUserInCategoryTimeline(BaseRedisTimelineStorage):
    key_format = "u_c_tl:%(category_id)s"
    def __init__ (self, category_id):
        self.key = self.key_format % {'category_id': category_id}
        super().__init__(self.key)

    @classmethod
    def get_activities_from_categories(cls, categories_id):
        store = RedisSet()
        activities = []
        for i in range(0, len(categories_id)):
            key = cls.key_format % {'category_id': categories_id[i]}
            store.set_key(key)
            items = store.get_all()
            
            #removing this line can make everything crash.
            items = [int(item.decode('utf-8')) for item in items]
            activities.extend(items)
        return activities

    @classmethod
    def add_to_many(cls, categories_id, activity_id):
        store = RedisSet()
        for i in range(0, len(categories_id)):
            key = cls.key_format % {'category_id': categories_id[i]}
            store.set_key(key)
            store.add(activity_id)
    
    
if __name__ == '__main__':
    r = RedisUserInCategoryTimeline
    print(r.get_activities_from_categories([1, 2, 4]))
