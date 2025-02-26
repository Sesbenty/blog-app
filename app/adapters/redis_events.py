from dataclasses import asdict
import json
import redis

from app import config
from app.domain.events import Event

r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


def publish(channel, event: Event):
    r.publish(channel, json.dump(asdict(event)))
