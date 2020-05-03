from flask_env import MetaFlaskEnv


class Config(metaclass=MetaFlaskEnv):
    ENV_LOAD_ALL = True
    FLASK_APP = 'app'
    FLASK_ENV = 'production'
    PREFERRED_URL_SCHEME = 'https'
    REDIS_URL = 'redis://localhost'
    JSON_SORT_KEYS = False
