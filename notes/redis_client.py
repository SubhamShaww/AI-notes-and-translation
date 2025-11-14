import os, redis

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)