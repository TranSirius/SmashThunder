import time
import datetime
import uuid

class CurrentTime:
    def __call__(self):
        dtime = datetime.datetime.now()
        unix_time = time.mktime(dtime.timetuple()) * 1000 - 60000
        return unix_time

class UUID:
    def __call__(self):
        return "".join(str(uuid.uuid1()).split("-")[:-1])