# _*_ coding: utf-8 _*_
__author__ = 'flyingV.zy'

from flask import Flask, Response, send_file, jsonify
from pymongo import MongoClient
import api.goods as goods
import api.image as image
import io
import json

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


if __name__ == '__main__':
    app.run(debug=True)
