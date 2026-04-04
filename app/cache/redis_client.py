import redis
import json
from app.core.config import settings

redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses = True)

def get_cache(key : str):
    data  = redis_client.get(key)
    if data:
        return json.loads(data)
    
    return None


def set_cache(key : str, value : dict, expire : int = 60):
    redis_client.setex(key, expire, json.dumps(value))