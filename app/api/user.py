__author__ = 'flyingV.zy'


def get_cart(db, openid):
    if db.users.find({'openid': openid}).count() == 0:
        db.users.insert_one({
            'openid': openid,
            'cart': []
        })
        return []
    else:
        cart = []
        try:
            for goods in db.users.find({'openid': openid}):
                cart.append({
                    'goods_uuid': goods.uuid,
                    'count': goods.count
                })
        except ValueError:
            print(ValueError)
        finally:
            return cart


def update_cart(db, openid, updateCart):
    return 'todo'
    # todo


def add_to_cart(db, openid, goods):
    return 'todo'
