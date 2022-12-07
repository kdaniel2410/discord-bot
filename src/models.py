import os
from datetime import datetime
from dotenv import load_dotenv
from peewee import *

load_dotenv()
db = SqliteDatabase(os.environ['DATA_DIR'] + 'db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Tag(BaseModel):
    tag = CharField(unique=True)
    body = TextField()
    created_by = BitField()
    guild_id = BitField()
    created_at = DateTimeField(default=datetime.now)


db.connect()
db.create_tables([Tag])
