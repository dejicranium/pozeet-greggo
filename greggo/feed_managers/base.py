from greggo.feed.base import UserFeed
from greggo.storage.redis import user_followings_storage
from greggo import tasks
from greggo.storage.redis.structures.set import RedisSet
from greggo.storage.redis.timeline_storage import RedisCategoryTimelineStorage, RedisUserInCategoryTimeline
from greggo.storage.redis.user_followings_storage import *
import random

class FeedManager: 
    user_feed_class = UserFeed

    def __init__(self, user_id):
        self.user_id = user_id
        self.followers_id = user_followings_storage.UserFollowers(self.user_id).get_followers()

    def create_activity(self, activities, subscriptions):
        """
            I think we should also fanout the activity to every category that the user belongs
        """
        result = tasks.app.send_task('tasks.fanout_activities', args=(self.user_id, self.followers_id, activities, subscriptions))

    def remove_activities(self, activities):
        tasks.app.send_task('task.remove_activities', args=(self.user_id, self.followers_id, activities))

    def get_user_feed(self):
        user_feed = UserFeed(self.user_id)
        return user_feed.get_activities()

    def get_categories_feed(self, categories_id):
        activities = []
        for category in categories_id: 
            category_feed = RedisCategoryTimelineStorage(category)
            category_activities = category_feed.get_feed()
            activities.extend(category_activities)
        return set(activities)

    def get_user_in_categories_feeds(self, categories_id):
        activities = []
        feed = RedisUserInCategoryTimeline
        activities = feed.get_activities_from_categories(categories_id)
        return activities
            

    def get_all_feeds(self, categories_id):
        user_in_categories_feeds_activities = self.get_user_in_categories_feeds(categories_id)
        
        user_feed_activities = self.get_user_feed()
        """
        category_feed_activities = self.get_categories_feed(categories_id)
        user_in_categories_feeds_activities = self.get_user_in_categories_feeds(categories_id)
        if not user_in_categories_feeds_activities:
            user_in_categories_feeds_activities = []
        user_feed_activities.extend(category_feed_activities)
        user_feed_activities.extend(user_in_categories_feeds_activities)
        """
        return user_in_categories_feeds_activities
        
        