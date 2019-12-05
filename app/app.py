# _*_ coding: utf-8 _*_
__author__ = 'flyingV.zy'

from flask import Flask, jsonify, request
from pymongo import MongoClient
import json
import requests
import config.setting as setting
from api.activity import Activity
import logging
from logging.handlers import TimedRotatingFileHandler

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
    try:
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        param = {
            'appid': setting.APP_ID,
            'secret': setting.APP_SECRET,
            'js_code': user_code,
            'grant_type': 'authorization_code'
        }
        res = requests.get(url, param, proxies=setting.proxy)
        # logging
        logging.debug(res.text)
        return res.text
    except Exception as e:
        logging.exception(e)


@app.route("/getMainPageActivity/", methods=['GET'])
def get_main_page_activity():
    try:
        all_activity = []
        openid = ''
        if request.method == 'GET':
            openid = request.args['openid']
            if len(str(openid)) < 25:
                return jsonify([])
            all_activity = activity.getMainPageActivity(openid)
        # 首页logging
        logging.debug(openid)
        return jsonify(all_activity)
    except Exception as e:
        logging.exception(e)


@app.route("/newActivity/", methods=['POST'])
def post_new_activity():
    if request.method == 'POST':
        try:
            data = json.loads(str(request.data, 'utf-8'))
            openid = data['openid']
            userInfo = data['userInfo']
            activityToAdd = data['activityToAdd']
            activity.postNewActivity(openid=openid, userInfo=userInfo, activity=activityToAdd)
            # 发布新活动logging
            logging.debug(openid)
            return jsonify({'success': True})
        except Exception as e:
            logging.exception(e)
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
            act = activity.getActivity(activityId)
            # 参加活动logging
            logging.debug(openid)
            return jsonify({'success': True, 'activity': act})
        except Exception as e:
            logging.exception(e)
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
            # 更新坐标logging
            logging.debug(openid)
            return jsonify(res)
        except Exception as e:
            logging.exception(e)
            return jsonify({'success': False, 'allLocation': []})
    elif request.method == 'GET':
        try:
            openid = request.args['openid']
            activityId = request.args['activityId']
            allMember = activity.getOneActivityAllMember(openid, activityId)
            # 获取位置信息logging
            logging.debug(openid)
            return jsonify(allMember)
        except Exception as e:
            logging.exception(e)
            return jsonify([])


@app.route("/activityDetail/", methods=['GET'])
def getActivityDetail():
    re = {'success': False}
    try:
        if request.method == 'GET':
            activityId = request.args['activityId']
            openid = request.args['openid']
            tmp = activity.getActivity(activityId)
            if tmp:
                re['success'] = True
                re['activity'] = tmp
            logging.debug(openid)
            return jsonify(re)
    except Exception as e:
        logging.exception(e)
        return jsonify(re)


@app.route("/myActivity/", methods=['GET'])
def getUserAct():
    re = {'success': False}
    try:
        if request.method == 'GET':
            openid = request.args['openid']
            act = activity.getUserAct(openid)
            if act:
                re['success'] = True
                re['activity'] = act
            logging.debug(openid)
            return jsonify(re)
        else:
            print(re)
            return jsonify(re)
    except Exception as e:
        logging.exception(e)


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
            logging.debug(openid)
            return jsonify(re)
        except Exception as e:
            logging.exception(e)
            return jsonify(re)
    else:
        print(re)


def logging_config():
    # 定义日志输出格式
    # fmt_str = '%(asctime)s[level-%(levelname)s][%(name)s][%(funcName)s][%(lineno)s]:%(message)s'
    # 初始化
    logging.basicConfig()

    # 创建TimedRotatingFileHandler处理对象
    # 间隔2(Hour)创建新的名称为myLog%Y%m%d_%H%M%S.log的文件，并一直占用myLog文件。
    fileshandle = logging.handlers.TimedRotatingFileHandler('flaskLog', when='H', interval=2, backupCount=2000)
    # 设置日志文件后缀，以当前时间作为日志文件后缀名。
    fileshandle.suffix = "%Y%m%d_%H.log"
    # 设置日志输出级别和格式
    fileshandle.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(fmt_str)
    # fileshandle.setFormatter(formatter)
    # 添加到日志处理对象集合
    logging.getLogger('').addHandler(fileshandle)


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)

    # logging
    # logging_config()
    # app.logger.setLevel()
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)