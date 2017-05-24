from squares.ext import redis

from squares.models.play.table import Table


class TableController:
    TABLE_MAX = 1024
    TABLE_ID = 'table_id_{}'

    def __init__(self, table_id):
        self.table = Table.get_by_id(table_id)

    def join(self, player_id):
        self.table.join(player_id)

    def step(self, schema_id, position):
        return

    @property
    def squares(self):
        return self.table.situation()
