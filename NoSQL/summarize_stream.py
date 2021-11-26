from pymongo import MongoClient
# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
result = client['timeseriesdemo']['weather'].aggregate([
    {
        '$project': {
            'ts': {
                '$dateToParts': {
                    'date': '$ts'
                }
            }, 
            'source': 1, 
            'temp': 1, 
            'windSpeed': 1
        }
    }, {
        '$group': {
            '_id': {
                'source': '$source', 
                'year': '$ts.year', 
                'month': '$ts.month', 
                'day': '$ts.day', 
                'hour': '$ts.hour', 
                'minute': '$ts.minute', 
                'second': {
                    '$multiply': [
                        {
                            '$floor': {
                                '$divide': [
                                    '$ts.second', 10
                                ]
                            }
                        }, 10
                    ]
                }
            }, 
            'avgTemp': {
                '$avg': '$temp'
            }, 
            'avgWindSpeed': {
                '$avg': '$windSpeed'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'source': '$_id.source', 
            'temp': {
                '$round': [
                    '$avgTemp', 1
                ]
            }, 
            'windSpeed': {
                '$round': [
                    '$avgWindSpeed', 1
                ]
            }, 
            'ts': {
                '$dateFromParts': {
                    'year': '$_id.year', 
                    'month': '$_id.month', 
                    'day': '$_id.day', 
                    'hour': '$_id.hour', 
                    'minute': '$_id.minute', 
                    'second': '$_id.second'
                }
            }
        }
    }, {
        '$merge': {
            'into': 'weather_10s', 
            'whenMatched': 'replace', 
            'whenNotMatched': 'insert'
        }
    }
])