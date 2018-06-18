from peewee import (
    PostgresqlDatabase, Model, TextField,
    DateTimeField, IntegerField
)

from config import PG_CONN

db = PostgresqlDatabase(**PG_CONN)


class BaseModel(Model):
    class Meta:
        database = db


class Chats(BaseModel):
    id = IntegerField(unique=True)


class Messages(BaseModel):
    owner = IntegerField()
    text = TextField()
    chat_id = IntegerField()
    send_dt = DateTimeField()


def init_db():
    tables = [Chats, Messages]
    for t in tables:
        if t.table_exists():
            t.drop_table()
        t.create_table()


if __name__ == '__main__':
    init_db()
    print('Tables created')
