# _*_ coding: utf-8 _*_
__author__ = 'flyingV.zy'

from flask import Flask, Response, send_file, jsonify, request
from pymongo import MongoClient
import api.goods as goods
import api.image as image
import io
import json
import requests
import config.setting as setting
import api.user as user
from api.activity import Activity

mongodb = MongoClient('localhost', 27017)
db = mongodb.flask_1009
activity = Activity(db)

app = Flask('mini')


@app.route("/test", methods=['GET'])
def get_test():
    return 'test success!'


@app.route("/", methods=['GET'])
def get_index():
    return 'welcome to my bike life!'


@app.route("/login/<user_code>", methods=['GET'])
def get_openid(user_code):
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    param = {
        'appid': setting.APP_ID,
        'secret': setting.APP_SECRET,
        'js_code': user_code,
        'grant_type': 'authorization_code'
    }
    res = requests.get(url, param, proxies=setting.proxy)
    return res.text


@app.route("/getMainPageActivity/", methods=['GET'])
def get_main_page_activity():
    all_activity = []
    if request.method == 'GET':
        openid = request.args['openid']
        if len(str(openid)) < 25:
            return jsonify([])
        all_activity = activity.getMainPageActivity(openid)
    return jsonify(all_activity)


@app.route("/newActivity/", methods=['POST'])
def post_new_activity():
    if request.method == 'POST':
        try:
            data = json.loads(str(request.data, 'utf-8'))
            openid = data['openid']
            userInfo = data['userInfo']
            activityToAdd = data['activityToAdd']
            activity.postNewActivity(openid=openid, userInfo=userInfo, activity=activityToAdd)
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            return jsonify({'success': False})


@app.route("/takeActivity/", methods=['POST'])
def post_one_activity():
    if request.method == 'POST':
        try:
            data = json.loads(str(request.data, 'utf-8'))
            openid = data['openid']
            userInfo = data['userInfo']
            activityId = data['activityId']
            activity.takeOneActivity(openid, userInfo, activityId)
            return jsonify({'success': True})
        except Exception:
            return jsonify({'success': False})


@app.route("/updateLocation/", methods=['POST'])
def update_location():
    if request.method == 'POST':
        try:
            data = json.loads(str(request.data, 'utf-8'))
            openid = data['openid']
            location = data['location']
            activityId = data['activityId']
            activity.updateUserLocation(openid, location)
            res = {
                'success': True,
                'allLocation': activity.getOneActivityAllMember(openid, activityId)
            }
            return jsonify(res)
        except Exception:
            print(Exception)
            return jsonify({'success': False, 'allLocation': []})
    elif request.method == 'GET':
        try:
            openid = request.args['openid']
            activityId = request.args['activityId']
            allMember = activity.getOneActivityAllMember(openid, activityId)
            return jsonify(allMember)
        except Exception:
            return jsonify([])


@app.route("/activityDetail/", methods=['GET'])
def getActivityDetail():
    re = {'success': False}
    if request.method == 'GET':
        activityId = request.args['activityId']
        tmp = activity.getActivity(activityId)
        if tmp:
            re['success'] = True
            re['activity'] = tmp
        print(re)
        return jsonify(re)
    else:
        return jsonify(re)


@app.route("/myActivity/", methods=['GET'])
def getUserAct():
    re = {'success': False}
    if request.method == 'GET':
        openid = request.args['openid']
        act = activity.getUserAct(openid)
        if act:
            re['success'] = True
            re['activity'] = act
        print(re)
        return jsonify(re)
    else:
        print(re)
        return jsonify(re)


@app.route("/quiteActivity/", methods=['POST'])
def quiteActivity():
    re = {'success': False}
    if request.method == 'POST':
        try:
            data = json.loads(str(request.data, 'utf-8'))
            openid = data['openid']
            activityId = data['activityId']

            activity.delUserFromActivity(activityId, openid)

            re = {
                'success': True
            }
            return jsonify(re)
        except Exception as e:
            print(e)
            return jsonify(re)
    else:
        print(re)


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(debug=True, host='127.0.0.1', port=5000)
