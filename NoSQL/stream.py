from pymongo import MongoClient
from datetime import datetime
from numpy import random
import time

client = MongoClient("mongodb://localhost:27017")
db = client.timeseriesdemo

sources = [11,22,33,44,55,66,77,88,99]
meantemps = [27,31,40,22,11,26,33,7,35]
meanwindspeeds = [22,14,10,30,20,25,5,13,19]

while True:
	docs = []
	
	for i in range(100):
		for s, t, w in zip(sources, meantemps, meanwindspeeds):
			docs.append(
				{
					"source" : s,
					"temp" : round(random.normal(t, 1), 1),
					"windSpeed" : round(random.normal(w, 2), 1),
					"ts" : datetime.utcnow()
				}
			)
		time.sleep(0.001)
	db.weather.insert_many(docs)