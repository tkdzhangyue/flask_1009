__author__ = 'flyingV.zy'
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO
import bson.binary


def get_img(db, image_id: str):
    img = db.images.find_one({'uuid': image_id})['img']
    return img


def resize_img(img_b, width, height, quality=85):
    img = Image.open(BytesIO(img_b))
    size = (width, height)
    img.thumbnail(size)
    img_b = BytesIO()
    img.save(img_b, format='JPEG')
    return img_b.getvalue()


if __name__ == "__main__":
    from pymongo import MongoClient

    mongodb = MongoClient('localhost', 27017)
    db = mongodb.flask_1009

    b1 = bson.binary.Binary(open('../static/images/3F.jpg', 'rb').read())
    im = resize_img(b1, 150, 150)
    im.save('../static/3_150.jpg', 'JPEG')
