from peewee import *

db = SqliteDatabase('logs.db')


class User(Model):
    username = CharField(unique=True)

    class Meta:
        database = db


class Log(Model):
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
