__author__ = 'flyingV.zy'


def get_one_goods(db):
    goods = db.data
    item = goods.find_one({'id': 1})
    return item


def get_main_page_goods(db):
    all_goods = db.goods.find({'id': {'$lt': 20}})
    page = []
    for good in all_goods:
        del good['_id']
        # good['main_img']['img'] = good['main_img']['img'].decode()
        page.append(good)
    return page


if __name__ == "__main__":
    from pymongo import MongoClient

    mongodb = MongoClient('localhost', 27017)
    db = mongodb.flask_1009
    get_one_goods(db)
