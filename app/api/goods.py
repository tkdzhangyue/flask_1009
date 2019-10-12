__author__ = 'flyingV.zy'


def get_one_goods(db):
    goods = db.data
    item = goods.find_one({'id': 1})
    return item


def get_main_page_goods(db):
    all_goods = []
    for good in db.goods.find():
        del good['_id']
        all_goods.append(good)
    return all_goods


if __name__ == "__main__":
    from pymongo import MongoClient

    mongodb = MongoClient('localhost', 27017)
    db = mongodb.flask_1009
    get_one_goods(db)
