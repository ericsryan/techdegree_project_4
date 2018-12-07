from peewee import *

db = SqliteDatabase('diary.db')


class User(Model):
    username = CharField()

    class Meta:
        database = db


class Log(Model):
    username = CharField()
    task_date = DateTimeField()
    task_title = CharField()
    task_time = IntegerField()
    task_notes = TextField()

def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)
