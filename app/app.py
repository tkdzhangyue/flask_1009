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

mongodb = MongoClient('localhost', 27017)
db = mongodb.flask_1009

app = Flask(__name__)


@app.route('/')
def index():
    all_goods = goods.get_main_page_goods(db)

    # return send_file(io.BytesIO(img), mimetype="image/png")
    return jsonify(all_goods)
    # return 'hello'


@app.route("/image/<image_id>", methods=['GET'])
def get_one_image(image_id):
    img = image.get_img(db, image_id)
    return send_file(io.BytesIO(img), mimetype="image/jpg")


@app.route("/goods/<goods_id>", methods=['GET'])
def get_goods_details(goods_id):
    goods_images = goods.get_goods_detail(db, goods_id)
    return jsonify(goods_images)


@app.route("/login/<user_code>", methods=['GET'])
def get_openid(user_code):
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    param = {
        'appid': setting.APP_ID,
        'secret': setting.APP_SECRET,
        'js_code': user_code,
        'grant_type': 'authorization_code'}
    return requests.get(url, param, proxies=setting.proxy).text


@app.route("/cart/", methods=['GET', 'POST'])
def cart():
    if request.method == 'GET':
        openid = request.args['openid']
        cart = user.get_cart(db, openid)
        return jsonify(cart)
    elif request.method == 'POST':
        data = json.loads(str(request.data, 'utf-8'))
        openid = data['openid']
        addedGodds = data['addedGoods']
        if addedGodds:
            res = user.add_to_cart(db, openid, addedGodds)
        else:
            updatedCart = data['cart']
            res = user.update_cart(db, openid, updatedCart)
        return res


@app.route("/address/", methods=['GET', 'POST'])
def get_user_address():
    if request.method == 'GET':
        openid = request.args['openid']
        address_list = []
        user_info = db.users.find_one({'openid': openid})
        try:
            address_list = user_info['address_list']
        except Exception:
            print(Exception)
        return jsonify(address_list)
    elif request.method == 'POST':
        return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
