# _*_ coding: utf-8 _*_
__author__ = 'flingV.zy'
import bson.binary


def test_upload_image(db):
    goods = db.data
    img1 = bson.binary.Binary(open('../static/images/1.png', 'rb').read())
    print(img1)

    goods.insert({'id': 1, 'images': [{'img': img1}]})


if __name__ == "__main__":
    from pymongo import MongoClient
    mongodb = MongoClient('localhost', 27017)
    db = mongodb.flask_1009
    test_upload_image(db)
