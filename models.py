"""Database for the Work Log program."""

from peewee import *

db = SqliteDatabase('logs.db')


class User(Model):
    """Table that holds the user's username."""

    username = CharField(unique=True)

    class Meta:
        database = db


class Log(Model):
    """Table that hold the work logs."""
    username = CharField()
    task_date = DateTimeField()
    task_title = CharField()
    task_time = IntegerField()
    task_notes = TextField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([User, Log], safe=True)
    if User.select().count() >= 1:
        users = User.select()
        for user in users:
            user.delete_instance()
    return True
