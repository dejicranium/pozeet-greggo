import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 

from greggo.feed.base import UserFeed
from celery import Celery
from greggo.storage.redis.timeline_storage import (
        RedisCategoryTimelineStorage, 
        RedisUserInCategoryTimeline
                                                )

app = Celery('tasks', 
            broker='pyamqp://guest@localhost//',)

"""Please note that activities here are integer ids"""

@app.task
def fanout_activities(user_id, follower_ids, activities, subscriptions=None):
    #first add to user_feed
    user_feed = UserFeed(user_id)
    user_feed.add_activities(activities)

    #then,fanout to followers_feed
    for follower in follower_ids: 
        follower_feed = UserFeed(follower)
        follower_feed.add_activities(activities)

    #MISSION: optionally add to 5 random categories that the user follows
    #EXPL: this enables user to easily get the activities of users that they are not following# 
    if subscriptions:
        user_in_category_feed = RedisUserInCategoryTimeline
        user_in_category_feed.add_to_many(subscriptions, activities)

@app.task
def remove_acitivities(user_id, acitivities):
    user_feed = UserFeed(user_id)
    user_feed.remove_activities(activities)
