import time
import json
import random

from squares.ext import redis
from squares.utils.dis_mutex import dist_mutex_context


class Table:
    """
    table_group: {
        '1': {
            'player_id': [11, 12, 13, 14],
            'turn': 1,
            'square': [[], ...],
            'timestamp': 142322....,
        }
    }
    """

    ID_FORMAT = 'table_id'
    TABLE_FORMAT = 'table_{}'
    TABLE_GROUP = 'table_group'
    PLAYER_FORMAT = 'table_{}_player'
    PLAYER_ID = 'player_id'

    def __init__(self, table_id):
        self.table_id = table_id
        self.table_info = json.loads(redis.hget(self.TABLE_GROUP, table_id))

    def id_key(self, table_id):
        return redis.get(self.ID_FORMAT.format(table_id))

    @classmethod
    def get_by_id(cls, table_id):
        return cls(table_id)

    def situation(self):
        if self.is_started:
            return self.table_info.get('square')

    @property
    def player_num(self):
        return len(self.players)

    @property
    def players(self):
        return self.table_info.get('players', [])

    @property
    def is_started(self):
        return self.table_info.get('turn', 0) > 0 and \
               len(self.table_info['player_id']) >= 2

    @classmethod
    def get_all(cls):
        return redis.hkeys(cls.TABLE_GROUP)

    @classmethod
    def create_table(cls):
        table_id = redis.incr(cls.ID_FORMAT, 1)
        table_info = dict(timestamp=int(time.time()), turn=0)
        redis.hset(cls.TABLE_GROUP, table_id, table_info)
        return table_id

    def commit(self):
        redis.hset(self.TABLE_GROUP, self.table_id, self.table_info)

    def start(self):
        if not self.is_started:
            self.table_info['square'] = [[0] * 16] * 16
            self.table_info['turn'] = random.randint(1, self.player_num)
            self.commit()
            return True
        return False

    def join(self):
        with dist_mutex_context('join_table_id_{}'.format(self.table_id), 10) \
                as lock:
            if lock:
                player_id = redis.incr(self.PLAYER_ID, 1)
                if self.player_num <= 4:
                    self.table_info.setdefault('players', []).append(player_id)
                    self.commit()
                    return self.table_id, player_id

    def put(self, player_id, schema):
        pass
