import time
import json
import random

from squares.ext import redis
from squares.utils.dis_mutex import dist_mutex_context
from squares.errors.table import TakeError, JoinTableError, StartError

TABLE_LEN = 20


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
        print(table_info)
        self.table_id = table_id
        self._table_info = table_info
        self.players = table_info['players']
        self.owner = table_info['owner']

    @classmethod
    def get_all(cls):
        all_table = redis.hgetall(cls.TABLE_GROUP)
        now = int(time.time())
        return [k.decode() for k, v in all_table.items() if int(v) > now]

    @classmethod
    def get_by_id(cls, table_id):
        table_info = redis.get(table_id)
        if table_info:
            table = cls()
            print(table_info.decode('utf-8').replace('\'', '"'))
            table.prepare(table_id, json.loads(
                table_info.decode('utf-8').replace('\'', '"')))
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
        if redis.set(table_id, json.dumps(table_info), ex=3600):
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

    @property
    def turn(self):
        return self._table_info['turn']

    def commit(self):
        if self.table_id and self._table_info:
            redis.set(self.table_id, self._table_info, ex=3600, xx=True)

    def start(self):
        with dist_mutex_context('start_'.format(self.table_id), 3) as locked:
            if locked:
                if len(self.players) < 2:
                    raise StartError('Poor players!')
                if self._table_info['turn'] != 0:
                    raise StartError('The Game has been started!')

                self._table_info['square'] = [[0] * TABLE_LEN] * TABLE_LEN
                self._table_info['status'] = [1] * len(self.players)
                self._table_info['turn'] = random.randint(
                    1, len(self.players))
                self.commit()

    def join(self, player_id):
        with dist_mutex_context('join_{}'.format(self.table_id), 3) as locked:
            if locked:
                if player_id in self.players:
                    return
                if self.is_started:
                    raise JoinTableError('The Game has been started!')
                if len(self.players) == 4:
                    raise JoinTableError('This Table is full!')

                self.players.append(player_id)
                self.commit()
                return
        raise JoinTableError('Network error, please try again!')

    def step(self, axises, n):
        if n != self._table_info['turn']:
            raise TakeError('Not your turn!')
        self._set_chess(axises, n)

        print('step:')
        print(axises)
        self._next_turn()

        self.commit()

    def _set_chess(self, axises, n):
        for axis in axises:
            if self._table_info['square'][axis[0]][axis[1]] == 0:
                self._table_info['square'][axis[0]][axis[1]] = n
            else:
                raise TakeError('take error')

    def _next_turn(self):
        turn = self._table_info['turn']
        while True:
            turn = turn % len(self.players) + 1
            if self._table_info['status'][turn - 1]:
                self._table_info['turn'] = turn
                break

    def quit(self, player_id):
        for index, p_id in enumerate(self.players):
            if player_id == p_id:
                self._table_info['status'][index] = 0
                self._next_turn()
                self.commit()
                break
