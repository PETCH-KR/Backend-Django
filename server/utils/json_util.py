import json
from bson import ObjectId
import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, (datetime.datetime, datetime.date, datetime.time)):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def jsonify(data):
    return json.loads(json.dumps(data, cls=JSONEncoder))
