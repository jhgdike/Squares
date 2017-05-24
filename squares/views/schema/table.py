from marshmallow import fields, Schema


class TableSchema(Schema):
    """table schema"""
    table_id = fields.String()
    players = fields.List(fields.Integer())
    owner = fields.Integer()
    is_started = fields.Boolean()

table_schema = TableSchema()
