import datetime

from peewee import *

db = SqliteDatabase('logs.db')

class Log(Model):
    username = CharField(max_length=100)
    task_date = DateTimeField(default=datetime.datetime.now)
    task_title = CharField(max_length=255)
    task_time = IntegerField()
    task_notes = TextField()

    class Meta:
        database = db

class User(Model):
    username = CharField(max_length=100, unique=True)

    class Meta:
        database = db


def initialize():
    """Create the database and table if they do not exist."""
    db.connect()
    db.create_tables([Log, User], safe=True)
