from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    is_manager = fields.Bool()
    password_hash = fields.Str(load_only=True)
    token = fields.Str(dump_only=True)
    token_expiration = fields.DateTime(dump_only=True)

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
