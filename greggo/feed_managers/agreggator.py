from greggo.feed.base import UserFeed
from greggo.storage.redis.category_subscription import CategorySubscription
import redis
from repoll.models.main_models import User, Activity
import random


def get_activities_by_similar_users(request, users):
    activities = request.dbsession.query(User).filter(Activity.user_id.in_(users), Activit).distinct(Activity.user_id.activity).limit(len(users)).all()
    return activities


def get_latest_activities(request, user_id, already_shown, start=0, end=30):
    max_per_batch = 20 
    
    user_feed = UserFeed(user_id)
    activities = user_feed.get_activities()[0:start+end]
    activities = (int(activity.decode('utf-8')) for activity in activities)
    #remove the activities the user has already seen 
    activities = activities - already_shown

    if len(activities) < max_per_batch:
        user = request.dbsession.query(User).filter(User.id==user_ids).first()
        subscriptions = [subscription.category_id  for subscription in user.subscriptions]

        while(len(acitivities)) < max_per_batch:
            # get 5 users from the random category
            random_category = random.sample(subscriptions, 5)

            category = CategorySubscription(random_category)
            subscribers = category.get_subscribers()
            subscribers = [int(subscriber.decode('utf-8')) for subscriber in subscribers]
            
            random_similar_users = random.sample(subscribers, 5)
            
            #if category has no subscriber
            if random_similar_users < 1: 
                continue
            activities_by_similar_users = get_activities_by_similar_users(request, random_similar_users)
            activities = activities - activities_by_similar_users


    elif activities > max_per_batch: 
        activities = activities[0: max_per_batch] 
            


    return list(activities)


if __name__ == '__main__':
    print(get_latest_activities('so', 1, 2))

    
    