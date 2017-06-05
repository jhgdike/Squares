from marshmallow import fields, Schema


class TableSchema(Schema):
    """table schema"""
    table_id = fields.String()
    players = fields.List(fields.String())
    turn = fields.Integer()
    is_owner = fields.Boolean()
    is_start = fields.Boolean(default=False)
    squares = fields.List(fields.List(fields.Integer()))
    player_n = fields.Integer()
    status = fields.List(fields.Boolean())

table_schema = TableSchema()
