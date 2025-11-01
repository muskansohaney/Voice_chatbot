import redis, os
from dotenv import load_dotenv

load_dotenv()
r = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
print("Connected:", r.ping())
