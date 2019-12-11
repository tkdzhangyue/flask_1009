import logging
import time


class CronJob:
    db = None

    def __init__(self, db):
        self.db = db

    def delTimeOutActivity(self):
        try:
            cur_time = int(time.time() * 1000)
            self.db.activity.update_many({'activityInfo.activityDate': {'$lt': cur_time}}, {'$set': {'status': 9}})
            logging.info('del act')
        except Exception as e:
            logging.exception(e)
