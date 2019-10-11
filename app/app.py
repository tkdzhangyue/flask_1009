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
    # all_goods = goods.get_main_page_goods(db)

    # return send_file(io.BytesIO(img), mimetype="image/png")
    # return jsonify(all_goods)
    return 'hello'


@app.route("/image/<image_id>", methods=['GET'])
def get_one_image(image_id):
    img = image.get_img(db, image_id)
    return send_file(io.BytesIO(img), mimetype="image/jpg")


if __name__ == '__main__':
    app.run(debug=True)
