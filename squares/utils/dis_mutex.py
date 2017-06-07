import uuid
from datetime import datetime, timedelta
from contextlib import contextmanager

from squares.ext import cache


class DistMutex(object):
    """
    a simple dist mutex
    """

    def __init__(self, key):
        self._key = 'mutex_' + key
        self._expire_time = None

    @property
    def is_locked(self):
        if self._expire_time:
            return self._expire_time > datetime.now()
        else:
            return False

    def lock(self, timeout):
        if not self.is_locked:
            value = uuid.uuid1()
            now = datetime.now()
            cache.add(self._key, value, timeout)
            if value == cache.get(self._key):
                self._expire_time = now + timedelta(seconds=timeout)
                return True

    def unlock(self):
        if self.is_locked:
            cache.delete(self._key)
        self._expire_time = None


@contextmanager
def dist_mutex_context(key, timeout):
    mutex = DistMutex(key)
    try:
        mutex.lock(timeout)
        yield mutex.is_locked
    finally:
        mutex.unlock()
