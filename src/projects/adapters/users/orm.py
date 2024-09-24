from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime,
    Boolean, 
)
from sqlalchemy.orm import registry

#from projects import config
from projects.domain import user
from projects.entrypoints.flask import db

users = db.Table(
    "users",
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(64), index=True, unique=True),
    Column("email", String(120), index=True, unique=True),
    Column("is_manager", Boolean),
    Column("password_hash", String(256)),
    Column("token", String(32), index=True, unique=True),
    Column("token_expiration", DateTime),
)

def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(
        user.User, users
    )
