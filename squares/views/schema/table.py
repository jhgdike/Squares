from marshmallow import fields, Schema


class TableSchema(Schema):
    """table schema"""
    table_id = fields.String()
    players = fields.List(fields.String())
    turn = fields.Integer(default=0, attribute='player_n')
    is_owner = fields.Boolean()
    is_started = fields.Boolean()
    squares = fields.List(fields.List(fields.Integer()))
    player_n = fields.Integer()
    status = fields.List(fields.Boolean())

table_schema = TableSchema()
