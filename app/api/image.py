__author__ = 'flyingV.zy'


def get_img(db, image_id: str):
    img = db.images.find_one({'uuid': image_id})['img']
    return img


if __name__ == "__main__":
    from pymongo import MongoClient

    mongodb = MongoClient('localhost', 27017)
    db = mongodb.flask_1009
