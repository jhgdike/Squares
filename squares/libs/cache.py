from flask_cache.backends import RedisCache


def redis(app, config, args, kwargs):
    kwargs.update(dict(key_prefix=config['CACHE_KEY_PREFIX']))
    return RedisCache(*args, **kwargs)
