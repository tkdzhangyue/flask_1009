# _*_ coding: utf-8 _*_
__author__ = 'flingV.zy'
import bson.binary
import uuid
from datetime import datetime
from api.image import resize_img


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


def upload_new_goods(db, img_info):
    goods_id = str(uuid.uuid1())
    img80_id = str(uuid.uuid1())
    img150_id = str(uuid.uuid1())
    img200_id = str(uuid.uuid1())
    img400_id = str(uuid.uuid1())

    db.goods.insert_one({
        'goods_id': goods_id,
        'main_img': [
            {
                'width': 80,
                'uuid': img80_id,
            },
            {
                'width': 150,
                'uuid': img150_id,
            },
            {
                'width': 200,
                'uuid': img200_id
            }
        ],
        'images': [
            {
                'uuid': img400_id
            }
        ]
    })
    db.images.insert_many([
        {
            'uuid': img80_id,
            'img': img_info[0]['bytes'],
            'create_date': datetime.utcnow(),
        },
        {
            'uuid': img150_id,
            'img': img_info[1]['bytes'],
            'create_date': datetime.utcnow(),
        },
        {
            'uuid': img200_id,
            'img': img_info[2]['bytes'],
            'create_date': datetime.utcnow(),
        },
        {
            'uuid': img400_id,
            'img': img_info[3]['bytes'],
            'create_date': datetime.utcnow(),
        }
    ])


if __name__ == "__main__":
    from pymongo import MongoClient

    mongodb = MongoClient('localhost', 27017)
    db = mongodb.flask_1009
    b1 = bson.binary.Binary(open('../static/images/1F.jpg', 'rb').read())
    b2 = resize_img(b1, 80, 80)
    b3 = resize_img(b1, 150, 150)
    b4 = resize_img(b1, 200, 200)
    u1 = uuid.uuid1()
    img_info = [
        {
            'format': 'jpg',
            'width': 80,
            'bytes': b2
        },
        {
            'format': 'jpg',
            'width': 150,
            'bytes': b3
        },
        {
            'format': 'jpg',
            'width': 200,
            'bytes': b4
        },
        {
            'format': 'jpg',
            'width': 400,
            'bytes': b1
        }
    ]
    upload_new_goods(db, img_info)
