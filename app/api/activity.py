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
        elif userInfo != {}:
            self.updateOneUser(openid, userInfo)
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
                'activityInfo.allMember': userInfo
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

    def updateOneUser(self, openid, userInfo):
        self.db.users.update_one({
            'openid': openid
        }, {
            '$set': {
                'userInfo': userInfo
            }
        })

    def getActivity(self, acId):
        data = self.db.activity.find_one({'activityId': acId})
        if data:
            del data['_id']
        return data

    def getUserAct(self, openid):
        act_ite = self.db.activity.find({
            'activityInfo.allMember.openid': openid
        })
        re = []
        for act in act_ite:
            # 去掉路线数据
            del act['activityInfo']['polyline']
            re.append(act['activityInfo'])
        return re

    def delUserFromActivity(self, activityId, openid):
        # 确认活动是否只有一个人
        act = self.db.activity.find_one({'activityId': activityId})
        if len(act['activityInfo']['allMember']) == 0:
            self.db.activity.delete_one({'activityId': activityId})
        elif len(act['activityInfo']['allMember']) == 1:
            if act['activityInfo']['allMember'][0]['openid'] == openid:
                self.db.activity.delete_one({'activityId': activityId})
        else:
            act = [u for u in act['activityInfo']['allMember'] if u['openid'] != openid]
            self.db.activity.update_one({'activityId': activityId}, {
                '$set': {
                    'activityInfo.allMember': act
                }
            })
