from greggo.storage.redis.structures.sorted_set import RedisSortedSet
from greggo.config import REDIS_SERVER
import datetime
from dateutil import relativedelta
import time

def get_hours_difference(now, then):
    #get the time difference between when the acitivity was posted and when
    #it is being added to the storage   
    difference = relativedelta.relativedelta(now, then)
    return difference.hours

def get_rank_score(interactions, criteria, hours, weight):
    """
    @param: interactions are the totla interactions that the activity accrued
    @param: 'criteria' is the number of criteria that we are to use to judge
            the popularity of an activity"
    @param: 'hours' is the number of hours since the activity was published
    @param: 'weight' - each activity type carries various weights
    """
    return round((interactions + 2/criteria)/pow(hours+2, weight), 1)

class TrendingPollsStorage(RedisSortedSet):
    key = "tr_p"
    
    def __init__(self, redis=None):
        self.redis = redis or REDIS_SERVER
        super().__init__(self.key, self.redis)

    def add_poll(self, poll):
        """Each time a user adds a new poll, we insert into the trending
        storage to find out whether it has a place there
        
        Remember, it is a sorted set, so it remains unique
        """
        votes = poll.num_of_votes
        comments = poll.num_of_comments
        #shares = poll.num_of_shares
        #likes = poll.num_of_likes
        interactions = votes + comments
        date_added = poll.date_added
        now = datetime.datetime.utcnow()
        hours_past = get_hours_difference(now, date_added)
        poll_score = get_rank_score(interactions, 2, hours_past, 1.5)
        #add to redis sorted sorted for trending polls
        self.add([poll.id, poll_score])

    def get_polls(self, start=None, end=None):
        return self.get_all(start, end)

    def get_poll_score(self, poll_id): 
        return self.get_score(poll_id)


class TrendingCommentsStorage(RedisSortedSet):
    key = "tr_c"

    def __init__(self, redis=None):
        self.redis = redis or REDIS_SERVER
        super().__init__(self.key, self.redis)

    def add_comment(self, comment):
        criteria = 2        
        shares = comment.num_of_shares
        likes = comment.num_of_likes
        replies = 0

        if comment.num_of_replies: 
            replies = comment.num_of_replies
            criteria = 2
        
        interactions = shares + replies + likes

        hours_past = get_hours_difference(datetime.datetime.utcnow(), comment.date_added)
        comment_score = get_rank_score(interactions, criteria, hours_past, 1.5)
        
        self.add([comment.id, comment_score])

    def get_comments(self, start=None, end=None):
        return self.get_all(start, end)

    def get_comment_score(self, comment_id):
        return self.get_score(comment_id)


class TrendingOpinionsStorage(RedisSortedSet):
    key = "tr_o"

    def __init__(self, redis=None):
        self.redis = redis or REDIS_SERVER
        super().__init__(self.key, self.redis)
    

    def add_opinion(self, opinion):
        votes = opinion.num_of_votes
        shares = opinion.num_of_shares
        interactions = votes + shares

        criteria = 2
        
        hour_now = datetime.datetime.utcnow()
        hours_past = get_hours_difference(hour_now, opinion.date_added)
        
        opinion_score = get_rank_score(interactions, criteria, hours_past, 1.5)
        self.add([opinion.id, opinion_score])

    def get_opinions(self, start=None, end=None):
        return self.get_all(start, end)
    