import redis
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
#REDIS_SERVER = redis.Redis(host="http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com", port="6379")
REDIS_SERVER = redis.Redis()
def change_redis_connection():
    pass
