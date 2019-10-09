# _*_ coding: utf-8 _*_
__author__ = 'flyingV.zy'

from flask import Flask, Response, send_file
from pymongo import MongoClient
import api.goods as goods
import io

mongodb = MongoClient('localhost', 27017)
db = mongodb.flask_1009

app = Flask(__name__)


@app.route('/')
def index():
    one_goods = goods.get_one_goods(db)
    # print(one_goods)
    imgs = one_goods['images']
    img = imgs[0]['img']
    return send_file(io.BytesIO(img), mimetype="image/png")


if __name__ == '__main__':
    app.run(debug=True)
