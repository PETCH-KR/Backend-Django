import json
from bson import ObjectId
import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, (datetime.datetime, datetime.date, datetime.time)):
            print("here")
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def jsonify(data):
    return json.loads(json.dumps(data, cls=JSONEncoder))


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
