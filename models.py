from peewee import (
    SqliteDatabase, Model, TextField,
    DateTimeField, IntegerField
)

sqlite_db = SqliteDatabase('mailer.db')


class BaseModel(Model):
    class Meta:
        database = sqlite_db


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
    print('Таблицы создал')
