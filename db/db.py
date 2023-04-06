from peewee import *

# 连接sqlite3数据库
db = SqliteDatabase('./db/data.db')

class BaseModel(Model):
    class Meta:
        database = db

# 定义模型基类
class Discussion(BaseModel):
    id = TextField(primary_key=True)
    title = TextField()
    url = TextField()


db.connect()
db.create_tables([Discussion])


def is_discussion_exists(id):
    return Discussion.select().where(Discussion.id == id).exists()

def new_discussion(id, title, url):
    Discussion(id=id, title=title, url=url).save(force_insert=True)



