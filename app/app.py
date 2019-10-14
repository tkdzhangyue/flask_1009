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
        openid = request.form['openid']
        addedGodds = request.form['addedGoods']
        if addedGodds:
            user.add_to_cart(db, openid, addedGodds)
        else:
            updatedCart = request.form['cart']
            user.update_cart(db, openid, updatedCart)


if __name__ == '__main__':
    app.run(debug=True)
