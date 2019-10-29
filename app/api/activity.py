__author__ = 'flyingV.zy'

from pymongo import MongoClient


class Activity:
    db = None

    def __init__(self, db):
        self.db = db

    def getMainPageActivity(self, openid):
        re = []
        if self.db.users.find({'openid': openid}).count() == 0:
            self.createOneUser(openid, {})
        all = self.db.activity.find()
        for item in all:
            del item['_id']
            re.append(item)
        return re

    def postNewActivity(self, openid, userInfo, activity):
        userInfo = userInfo
        if self.db.users.find({'openid': openid}).count() == 0:
            self.createOneUser(openid, userInfo)
        # 更新用户信息
        self.db.users.update_one({'openid': openid}, {"$addToSet": {
            'activity': {'activityId': activity['activityId']}
        }})
        # 更新活动
        self.db.activity.insert_one({
            'activityId': activity['activityId'],
            'activityInfo': activity
        })

    def takeOneActivity(self, openid, userInfo, activityId):
        if self.db.users.find({'openid': openid}).count() == 0:
            self.createOneUser(openid, userInfo)
        # 更新用户
        self.db.users.update_one({'openid': openid}, {
            "$addToSet": {
                'activity': {
                    'activityId': activityId
                }
            }
        })
        # 更新活动
        self.db.activity.update_one({'activityId': activityId}, {
            "$addToSet": {
                'activityInfo': {
                    'allMember': {
                        'openid': openid,
                        'userInfo': userInfo
                    }
                }
            }
        })

    def updateUserLocation(self, openid, location):
        if self.db.location.find({'openid': openid}).count < 1:
            self.db.location.insert_one({'openid': openid, 'location': location})
        else:
            self.db.location.update_one({'openid': openid}, {
                "$set": {
                    location: {
                        'latitude': location['latitude'],
                        'longitude': location['longitude']
                    }
                }
            })

    def getOneActivityAllMember(self, openid, activityId):
        all_openid = []
        re = []
        activity = self.db.activity.find_one({'activityId': activityId})
        for member in activity['allMember']:
            all_openid.append(member.openid)
        for location in self.db.location.find({'openid': {"$in": all_openid}}):
            re.append(location['location'])
        return re

    def createOneUser(self, openid, userInfo):
        self.db.users.insert_one({
            'openid': openid,
            'userInfo': userInfo,
            'activity': []
        })
