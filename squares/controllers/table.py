from squares.ext import redis


class TableController:
    TABLE_MAX = 1024
    TABLE_ID = 'table_id_{}'

    def __init__(self):
        pass

    def table_key(self, table_id):
        return self.TABLE_ID.format(table_id)

    def tables(self):
        key = 'all_the_tables'
        return redis.get(key)

    def create_table(self):
        for i in range(1, self.TABLE_MAX):
            if redis.setnx(self.table_key(i), i):
                return i

    def join(self, table_id):
        """return: player_id, role_id"""
        if not redis.get(self.table_key(table_id)):
            raise Exception('Table is not exist!')
        role_id = int(
            redis.incr('table_id_{}_for_player'.format(table_id), 1))
        if role_id <= 4:
            player_id = int(redis.incr('player_id', 1))
            return player_id, role_id
        raise Exception('This Table is full!')

    def observer(self, table_id):
        return redis.get(self.table_key(table_id))
