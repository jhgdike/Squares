from squares.models.play.table import Table
from squares.models.schema import get_axis_by_schema_id
from squares.errors.table import OutRangeError, TakeError


class TableController:
    TABLE_MAX = 1024
    TABLE_ID = 'table_id_{}'

    def __init__(self, table_id, player_id=0):
        self.table_id = table_id
        self.table = Table.get_by_id(table_id)
        self.player_id = player_id
        self.players = self.table.players

    @property
    def player_n(self):
        if self.player_id:
            for index, player_id in enumerate(self.players):
                if player_id == self.player_id:
                    return index + 1

    @property
    def turn(self):
        return self.table.turn

    @property
    def is_owner(self):
        return self.player_n == 1

    @property
    def is_start(self):
        return self.table.is_started

    def start(self):
        if self.player_n != 1:
            raise TakeError('Only onwer can start the game!')
        if self.player_id != self.table.owner:
            raise TakeError('Your are not the onwer!')
        self.table.start()

    def join(self, player_id):
        self.table.join(player_id)
        self.player_id = player_id

    def step(self, schema_id, position, rotate=0, symmetry=False):
        axises = get_axis_by_schema_id(schema_id, position, rotate, symmetry)
        self._check(axises)

        self.table.step(axises, self.player_n)

    def quit(self):
        self.table.quit(self.player_id)

    def _check(self, axises):
        self.is_opposite = False
        for item in axises:
            self.is_legal(item)

        if not self.is_opposite:
            raise TakeError('Must be in the opposite of your chess!')

    def is_legal(self, axis):
        if not self._check_out(axis):
            raise OutRangeError('Out of range!')

        if self.squares[axis[0]][axis[1]]:
            raise TakeError('Wrong location!')

        self._check_touch(axis)
        self._check_opposite(axis)

    def _check_out(self, axis):
        return 0 < axis[0] < len(self.squares) and \
               0 < axis[1] < len(self.squares)

    def _check_touch(self, axis):
        for op in _touch:
            new_ax = [axis[0] + op[0], axis[1] + op[1]]
            if self._check_out(new_ax):
                if self.player_n == self._chess_n(new_ax):
                    raise TakeError('Adjacent to your chess!')
        return True

    def _check_opposite(self, axis):
        for op in _opposite:
            new_ax = [axis[0] + op[0], axis[1] + op[1]]
            if self._check_out(new_ax):
                if self.player_n == self._chess_n(new_ax):
                    self.is_opposite = True
                    break

    def _chess_n(self, axis):
        return self.squares[axis[0]][axis[1]]

    @property
    def squares(self):
        return self.table.situation()

    @property
    def status(self):
        return self.table.status

_touch = [
    [0, -1],
    [0, 1],
    [1, 0],
    [-1, 0],
]

_opposite = [
    [-1, -1],
    [1, 1],
    [-1, 1],
    [1, -1],
]
