
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
from greggo.storage.redis.timeline_storage import RedisUserTimelineStorage
from greggo.config import REDIS_SERVER


class BaseFeed: 
    storage = RedisUserTimelineStorage
    
    def __init__(self, key, redis_server=None):
        self.key = key
        self.redis_server = redis_server or REDIS_SERVER
        self.storage = RedisUserTimelineStorage

    def set_storage(self, storage_class):
        self.storage = storage_class

    def initialize_storage(self):
        return self.storage(self.key, self.redis_server)

    def add_activities(self, activity_and_score):
        self.storage.add_many(activity_and_score)
    
    def get_activities(self):
        activities = self.storage.get_many()
        #activity ids are stored as unicode in redis. So, we need to decode them.
        activities = [int(activity.decode('utf-8')) for activity in activities]
        return activities

    def remove_activities(self, activities):
        self.storage.remove_many(activities)


class UserFeed(BaseFeed):
    key_format = "u_fd:%(user_id)s"

    def __init__(self, user_id, redis_server=None):
        self.key = self.key_format % {'user_id': user_id}
        super().__init__(self.key, redis_server)
        #set the storage class
        self.set_storage(RedisUserTimelineStorage)
        self.storage = self.initialize_storage()


if __name__ == "__main__":
    print(UserFeed(1).get_activities())