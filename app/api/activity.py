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
        print(re)
        return re

    def postNewActivity(self, openid, userInfo, activity):
        userInfo = userInfo
        if self.db.users.find({'openid': openid}).count() == 0 and len(openid) > 6:
            self.createOneUser(openid, userInfo)
        # 更新用户信息
        self.db.users.update_one({'openid': openid}, {"$addToSet": {
            'activity': {'activityId': activity['activityId']}
        }})
        self.db.users.update_one({'openid': openid}, {"$set": {
            'userInfo': userInfo
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
        count = self.db.location.find({'openid': openid}).count()
        if count < 1:
            self.db.location.insert_one({'openid': openid, 'location': location})
        else:
            self.db.location.update_one({'openid': openid}, {
                "$set": {
                    'location': {
                        'latitude': location['latitude'],
                        'longitude': location['longitude']
                    }
                }
            })

    def getOneActivityAllMember(self, openid, activityId):
        all_openid = []
        re = []
        activity = self.db.activity.find_one({'activityId': activityId})
        for member in activity['activityInfo']['allMember']:
            all_openid.append(member['openid'])
        allLocation = self.db.location.find({'openid': {"$in": all_openid}})
        for location in allLocation:
            user = self.db.users.find_one({'openid': location['openid']})
            iconPath = user['userInfo']['avatarUrl']
            re.append({
                'location': location['location'],
                'iconPath': iconPath,
                'openid': location['openid']})
        return re

    def createOneUser(self, openid, userInfo):
        self.db.users.insert_one({
            'openid': openid,
            'userInfo': userInfo,
            'activity': []
        })
