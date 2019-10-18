__author__ = 'flyingV.zy'
from flask import jsonify


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
            user = db.users.find_one({'openid': openid})
            for goods in user['cart']:
                goods_info = db.goods.find_one({'goods_id': goods['goods_id']})
                cart.append({
                    'goods_id': goods['goods_id'],
                    'count': goods['count'],
                    'image': goods['image'],
                    'title': goods_info['title'],
                    'price': goods_info['price'],
                    'stock_num': goods_info['stock_num']
                })
        except ValueError:
            print(ValueError)
        finally:
            return cart


def update_cart(db, openid, updateCart):
    return 'todo'
    # todo


def add_to_cart(db, openid, goods_id):
    if db.users.find({'openid': openid}).count() == 0:
        get_cart(db, openid)
    try:
        image = db.goods.find_one({'goods_id': goods_id})['main_img'][0]
        db.users.update_one({'openid': str(openid)}, {
            "$addToSet": {
                'cart': {
                    'goods_id': str(goods_id),
                    'count': 1,
                    'image': image['uuid']
                }
            }
        })
        return jsonify({'success': True})
    except Exception:
        return jsonify({'success': False})


def update_address(db, openid, address):
    try:
        db.users.update_one({'openid': openid}, {
            "$set": {
                'address': {
                    'name': address['name'],
                    'tel': address['tel'],
                    'address': address['address']
                }
            }
        })
        return jsonify({'success': True})
    except Exception:
        return jsonify({'success': False})
