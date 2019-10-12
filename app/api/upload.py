# _*_ coding: utf-8 _*_
__author__ = 'flingV.zy'
import bson.binary
import uuid
from datetime import datetime


def test_upload_image(db):
    goods = db.goods
    img1 = bson.binary.Binary(open('../static/images/3.jpg', 'rb').read())
    print(img1)

    goods.insert({
        'id': 4,
        'main-img': {
            'format': 'jpg',
            'img': img1
        },
        'images': [
            {'format': 'jpg', 'img': img1},
            {'format': 'jpg', 'img': img1},
            {'format': 'jpg', 'img': img1},
            {'format': 'jpg', 'img': img1}
        ]
    })


def upload_image(db, goods_id, img_format: str, img: bytes):
    img_uuid = uuid.uuid1()
    if db.goods.find({'uuid': str(goods_id)}).count() == 0:
        db.goods.insert_one({
            'uuid': str(goods_id),
            'images': [
                {'uuid': str(img_uuid)}
            ]
        })
    else:
        db.goods.update_one({'uuid': str(goods_id)},
                            {"$push": {
                                'images': {
                                    'uuid': str(img_uuid)
                                }
                            }})

    db.images.insert_one({
        'create_date': datetime.utcnow(),
        'uuid': str(img_uuid),
        'format': img_format,
        'img': img
    })


if __name__ == "__main__":
    from pymongo import MongoClient

    mongodb = MongoClient('localhost', 27017)
    db = mongodb.flask_1009
    upload_image(db, 'd184a036-ec9c-11e9-84b2-4ccc6a382b99', 'jpg',
                 bson.binary.Binary(open('../static/images/444.jpg', 'rb').read()))
