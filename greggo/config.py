import redis
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
#REDIS_SERVER = redis.Redis(host="pozeet-redis-cluster.0jy3so.ng.0001.use2.cache.amazonaws.com", port="6379", ssl=True)
REDIS_SERVER = redis.Redis()
def change_redis_connection():
    pass
