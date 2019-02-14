from greggo.storage.redis.structures.hash import RedisHash
from greggo.config import REDIS_SERVER

class BaseVotersAgeStorage(RedisHash):
    def __init__(self, redis):
        super().__init__(redis)

    def add_age(self, age):
        self.set(self.key, {str(age)})
    
    def get_ages(self):
        return self.get_all(self.key)

    def increment_age(self, age):
        self.increment(self.key, age)


class PollVotersAgeStorage(BaseVotersAgeStorage):
    key_format = 'pv_a_s:%(poll_id)s'
    
    def __init__(self, poll_id, redis):
        self.key = self.key_format % {'poll_id': poll_id}
        self.redis = redis or REDIS_SERVER
        super().__init__(self.redis)


class OpinionVotersAgeStorage(BaseVotersAgeStorage):
    key_format = 'ov_a_s:%(opinion_id)s'

    def __init__(self, opinion_id, redis):
        self.key = self.key_format % {'opinion_id': opinion_id}
        self.redis = redis or REDIS_SERVER
        super().__init__(self.redis)

if __name__ == '__main__':
    v = VotersAgeStorage(1, REDIS_SERVER)
    print(v.get_ages())
    
    