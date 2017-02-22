import datetime
import os
import requests
from urlparse import urljoin

class Utility(object):
    @classmethod
    def get_celery_tasks(cls):
        retval = []
        celery_url = urljoin(os.getenv("FLOWER_HOST"), "api/tasks")
        result = requests.get(celery_url).json()
        for task in result.items():
            task_prefmt = {"id": task[0],
                           "name": task[1]["name"],
                           "args": str(task[1]["args"]),
                           "kwargs": str(task[1]["kwargs"]),
                           "started": Utility.u_to_8601(task[1]["started"]),
                           "tstamp": Utility.u_to_8601(task[1]["timestamp"]),
                           "state": task[1]["state"],
                           "exception": str(task[1]["exception"])}
            retval.append(task_prefmt)
        return retval

    @classmethod
    def u_to_8601(cls, unixtime):
        try:
            ret = datetime.datetime.fromtimestamp(float(unixtime)).isoformat()
        except TypeError:
            ret = "N/A"
        return ret
