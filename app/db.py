import json
from typing import Any, Optional
from typing_extensions import Protocol

from fakeredis import FakeStrictRedis
from redis import StrictRedis


class RedisMixin(Protocol):
    def get_json(self, key) -> Any:
        string = self.get(key)
        if string is None:
            return None
        return json.loads(string)

    def set_json(self, key, value, *args, **kwargs):
        return self.set(key, json.dumps(value), *args, **kwargs)


class FakeDb(FakeStrictRedis, RedisMixin):
    pass


class Db(StrictRedis, RedisMixin):
    pass


db: Optional[Db] = None

def init_db(app):
    global db
    redis_url = app.config['REDIS_URL']
    if redis_url == 'mock':
        app.logger.warning('Connecting to MOCK Redis')
        db = FakeDb()
    else:
        app.logger.debug(f'Connecting to Redis at {redis_url}')
        db = Db.from_url(redis_url)
    return db
