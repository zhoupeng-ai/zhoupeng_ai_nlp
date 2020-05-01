import numpy as np
import pymongo as mongo

client = mongo.MongoClient('localhost', 27017)

db = client['local']

col = db["test"]

exec = col.find_one()

xs = col.find()

for i in xs:
	print(i)
print(exec)
