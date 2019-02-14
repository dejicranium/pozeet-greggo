from greggo.storage.redis.structures.hash import RedisHash
from greggo.config import REDIS_SERVER

class BaseVotersGenderStorage(RedisHash):
    def __init__(self, poll_id, redis=None):
        self.redis = redis or REDIS_SERVER
        super().__init__(self.redis)


    def get_gender_votes(self):
        return self.get_all(self.key)
    
    def increment_gender_votes(self, gender):
        self.increment(self.key, gender)

    
class PollVotersGenderStorage(BaseVotersGenderStorage):
    key_format = 'pv_g_s:%(poll_id)s'
    
    def __init__(self, poll_id, redis=None):
        self.key = self.key_format % {'poll_id': poll_id}
        self.redis = redis or REDIS_SERVER
        super().__init__(self.redis)


class OpinionVotersGenderStorage(BaseVotersGenderStorage):
    key_format = 'ovc_g_s:%(opinion_id)s'
    
    def __init__(self, opinion_id, redis=None):
        self.key = self.key_format % {'opinion_id': opinion_id}
        self.redis = redis or REDIS_SERVER
        super().__init__(self.redis)






if __name__ == '__main__':
    v = PollVotersGenderStroage(1, REDIS_SERVER)
    print(v.get_gender_votes())