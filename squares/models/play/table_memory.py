import time
import random
from threading import Lock

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
    incr_table_id = 0
    ID_FORMAT = 'table_id'  #: only use for generate table id
    TABLE_GROUP = 'table_group'  #: all the table

    TABLE_FORMAT = 'table_{}'
    PLAYER_FORMAT = 'table_{}_player'
    PLAYER_ID = 'player_id'

    all_tables = {}
    __lock = Lock()

    def __init__(self, table_id, player_id):
        self._expire_at = int(time.time()) + 3600 * 3
        self._turn = 0
        self._owner = player_id
        self._table_id = table_id
        self._players = [player_id]

        self._status = None
        self._square = [[0] * TABLE_LEN for _ in range(TABLE_LEN)]

        self.__table_lock = Lock()

    def _table_info(self):
        return {
            'turn': self._turn,
            'players': self._players,
            'owner': self._owner,
            'expire_at': self._expire_at,
        }

    @property
    def expire_at(self):
        return self._expire_at

    @property
    def table_id(self):
        return self._table_id

    @property
    def players(self):
        return self._players

    @property
    def status(self):
        return self._status

    @property
    def owner(self):
        return self._owner

    @property
    def turn(self):
        return self._turn

    @classmethod
    def get_all(cls):
        now = int(time.time())
        return [k for k, v in cls.all_tables.items() if v.expire_at > now]

    @classmethod
    def get_by_id(cls, table_id):
        return cls.all_tables.get(table_id)

    @classmethod
    def create_table(cls, player_id):
        # add table_id to the group
        with cls.__lock:
            cls.incr_table_id += 1

        # create the table
        table_id = cls.TABLE_FORMAT.format(cls.incr_table_id)
        table = cls(table_id, player_id)
        cls.all_tables[table_id] = table
        return table

    def situation(self):
        if self.is_started:
            return self._square

    @property
    def is_started(self):
        return self._turn > 0 and len(self._players) >= 2

    def start(self):
        with self.__table_lock:
            if len(self._players) not in (2, 3, 4):
                raise StartError('Poor players!')
            if self._turn != 0:
                raise StartError('The Game has been started!')

            self._status = [1] * len(self._players)
            self._turn = random.randint(1, len(self._players))

    def join(self, player_id):
        with self.__table_lock:
            if player_id in self._players:
                return
            if self.is_started:
                raise JoinTableError('The Game has been started!')
            if len(self._players) == 4:
                raise JoinTableError('This Table is full!')

            self._players.append(player_id)
            return

    def step(self, axises, n):
        if n != self._turn:
            raise TakeError('Not your turn!')
        with self.__table_lock:
            self._set_chess(axises, n)

            # print('step:')
            # print(axises)
            self._next_turn()

    def _set_chess(self, axises, n):
        for axis in axises:
            if self._square[axis[0]][axis[1]] == 0:
                self._square[axis[0]][axis[1]] = n
            else:
                raise TakeError('take error, {}, squre: {}'.format(axises, self._square))

    def _next_turn(self):
        turn = self._turn
        while True:
            turn = turn % len(self._players) + 1
            if self._status[turn - 1]:
                self._turn = turn
                break

    def quit(self, player_id):
        with self.__table_lock:
            for index, p_id in enumerate(self._players):
                if player_id == p_id:
                    self._status[index] = 0
                    self._next_turn()
                    break
