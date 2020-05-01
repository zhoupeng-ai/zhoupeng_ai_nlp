import numpy as np
import pymongo as mongo
import datetime

client = mongo.MongoClient('localhost', 27017)
print(client)

db = client['local']
print(db)
dblist = client.list_database_names()

if 'local' in dblist:
	print("数据库已存在")
col = db["test"]
post = {"author": "zhoupeng",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}
exec = col.insert_one(post)
print(exec.inserted_id)