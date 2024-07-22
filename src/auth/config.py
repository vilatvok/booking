import redis


SECRET = 'dc9af13f8be66af4d21a51441df6751f'
redis_client = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True,
)
