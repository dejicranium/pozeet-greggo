from greggo.storage.redis.structures.set import RedisSet
from greggo.config import REDIS_SERVER
#from repoll.services.activity_service import get_user_activities

class BaseFollowings(RedisSet):
    def __init__(self, key, redis=None):
        super().__init__(key, redis)


class UserFollowings(BaseFollowings):
    key_format = 'u_fing:%(user_id)s'


    def __init__(self, user_id, redis=None):
        key = self.key_format % {'user_id': user_id}
        super().__init__(key, redis)

    def follow_user(self, followee_id):
        self.add(followee_id)

    def get_followees(self):
        followees =  self.get_all()
        followees = [int(followee.decode('utf-8')) for followee in followees]
        return followees

    def unfollow_user(self, followee_id):
        self.delete(followee_id)

    def is_following_user(self, followee_id):
        return self.exists(followee_id)


class UserFollowers(BaseFollowings):
    key_format = 'u_fll:%(user_id)s'

    def __init__(self, user_id, redis=None):
        key = self.key_format % {'user_id': user_id}
        super().__init__(key, redis)

    def get_followers(self):
        followers = self.get_all()
        followers =  [int(follower.decode('utf-8')) for follower in followers]
        return followers

    def add_new_follower(self, follower_id):
        self.add(follower_id)

    def remove_follower(self, follower_id):
        self.delete(follower_id)



class FollowingsManager:
    @classmethod
    def load_in_followers(cls, user_id, list_of_followers):
        followers_store = UserFollowers(user_id)
        followers_store.add_new_follower(list_of_followers)

    @classmethod
    def load_in_followees(cls, user_id, list_of_followees):
        followees_store = UserFollowings(user_id)
        followees_store.follow_user(list_of_followees)

    @classmethod
    def user_is_following(cls, user1_id, user2_id, redis=None):
        followings =UserFollowings(user1_id, redis)
        return followings.is_following_user(user2_id)

    @classmethod
    def follow_user(cls, user_id, to_follow_id):
        UserFollowings(user_id).follow_user(to_follow_id)
        UserFollowers(to_follow_id).add_new_follower(user_id)


    @classmethod
    def unfollow_user(cls, request, user_id, to_unfollow_id):
        UserFollowings(user_id).unfollow_user(to_unfollow_id)
        UserFollowers(to_unfollow_id).remove_follower(user_id)

        

        