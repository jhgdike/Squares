import time
import json
import random

from squares.ext import redis
from squares.utils.dis_mutex import dist_mutex_context
from squares.errors.table import BusyError, JoinTableError, StartError


class Table:
    """
    The model with one table.
    
    table_group: {
        'table_1': 142322....,
    }

    table_1: {
        'players': [11, 12, 13, 14],
        'turn': 1,  #: 0 not start. -1 over.
        'square': [[], ...],
    }
    """
    ID_FORMAT = 'table_id'  #: only use for generate table id
    TABLE_GROUP = 'table_group'  #: all the table

    TABLE_FORMAT = 'table_{}'
    PLAYER_FORMAT = 'table_{}_player'
    PLAYER_ID = 'player_id'

    def __init__(self):
        self.table_id = None
        self._table_info = None
        self.players = None
        self.owner = None

    def prepare(self, table_id, table_info):
        self.table_id = table_id
        self._table_info = table_info
        self.players = table_info['players']
        self.owner = table_info['owner']

    @classmethod
    def get_all(cls):
        all_table = redis.hgetall(cls.TABLE_GROUP)
        now = int(time.time())
        return [str(k) for k, v in all_table.items() if int(v) > now]

    @classmethod
    def get_by_id(cls, table_id):
        table_info = redis.get(table_id)
        if table_info:
            table = cls()
            table.prepare(table_id, json.loads(table_info))
            return table

    @classmethod
    def create_table(cls, player_id):
        # add table_id to the group
        table_id = cls.TABLE_FORMAT.format(redis.incr(cls.ID_FORMAT, 1))
        timestamp = int(time.time()) + 3600
        redis.hset(cls.TABLE_GROUP, table_id, timestamp)

        # create the table
        table_info = {
            'turn': 0,
            'players': [player_id],
            'owner': player_id,
        }
        if redis.set(table_id, table_info, ex=3600):
            table = cls()
            table.prepare(table_id, table_info)
            return table

    def situation(self):
        if self.is_started:
            return self._table_info.get('square')

    @property
    def is_started(self):
        return self._table_info.get('turn', 0) > 0 and \
               len(self.players) >= 2

    def commit(self):
        if self.table_id and self._table_info:
            redis.set(self.table_id, self._table_info, ex=3600)

    def start(self):
        with dist_mutex_context('start_'.format(self.table_id), 3) as locked:
            if locked:
                if len(self.players) < 2:
                    raise StartError('人数不足！')
                if self._table_info['turn'] != 0:
                    raise StartError('本局游戏已开始！')

                self._table_info['square'] = [[0] * 16] * 16
                self._table_info['turn'] = random.randint(
                    1, len(self.players))
                self.commit()

    def join(self, player_id):
        with dist_mutex_context('join_{}'.format(self.table_id), 3) as locked:
            if locked:
                if self.is_started:
                    raise JoinTableError('本局游戏已开始！')
                if len(self.players) == 4:
                    raise JoinTableError('本桌已满！')

                self.players.append(player_id)
                self.commit()
                return
        raise JoinTableError('请重新尝试!')

    def put(self, player_id, schema):
        pass
