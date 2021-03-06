import os
import jwt
import datetime
import json
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from accounts import add_account, authenticate_user, get_id_by_email
from inventory import get_all_items, get_items_by_category, get_item_by_id, get_total_pages, update_qty, add_item, admin_update_quantity
from orders import get_orders_by_user, get_tracking_by_order, new_order
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'tempsecretkey'

@app.route('/receiver', methods = ['POST'])
@cross_origin()
def worker():
	# read json + reply
	data = request.get_json()

	if add_account(data.get('name'), data.get('email'), data.get('password')):
		responseObject = {
			"success": True,
			"msg": "registered"
		}
	else:
		responseObject = {
		"success": False,
		"msg": "account with that email exists"
		}
	return make_response(jsonify(responseObject))

@app.route('/authenticate', methods = ['POST'])
@cross_origin()
def login():
	data = request.get_json()
	email = data.get('email')
	password = data.get('password')

	result = authenticate_user(email, password)

	if result is None:
		responseObject = {
			"success": False,
			"msg": "Incorrect password!"
		}
	else:
		id = result["id"]
		type = result["type"]
		token = jwt.encode({'user': email, 'pass': password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours = 24)}, \
			app.config['SECRET_KEY'])
		responseObject = {
			"success": True,
			"token": token.decode('UTF-8'),
			"user_id":id,
			"type":type
		}
	return make_response(jsonify(responseObject))


@app.route('/search', methods = ['POST'])
@cross_origin()
def search():
	data = request.get_json()
	keyword = data.get('keyword')
	page = data.get('page')
	items = get_items_by_category(keyword, page)
	totalPages = get_total_pages(keyword)
	if not items:
		responseObject = {
			"success": False,
			"msg": "no items in that category"
		}
	else:
		responseObject = {
			"success": True,
			"inventory": items,
			"pages":totalPages
		}
	return make_response(jsonify(responseObject))


@app.route('/orders', methods = ['POST'])
@cross_origin()
def get_orders():
	data = request.get_json()
	user_id = data.get('id')
	orders = get_orders_by_user(user_id)
	if not orders:
		responseObject = {
			"success": False,
			"msg": "no orders by this user"
		}
	else:
		responseObject = {
			"success": True,
			"orders": orders,
		}
	return make_response(jsonify(responseObject))


@app.route('/payment', methods = ['POST'])
@cross_origin()
def processOrder():
	data = request.get_json()
	#cart contains qty and item_id
	cart = data.get('cart')
	# print(cart)
	#user_id used for adding to order history
	user_id = data.get('user_id')
	total = data.get('total')
	weight = data.get('weight')
	if(data.get('truckDelivery')):
		delivery_method = "Truck"
	else:
		delivery_method = "Drone"

	delivery_status = "Processing"

	#find geocode for address
	address = data.get('address') + " " + data.get('city')+ " " + data.get('state') + " " + data.get('zip')

	if update_qty(json.loads(cart)) and new_order(user_id, cart, total, weight, address, delivery_method, delivery_status):
			responseObject = {
			"success":True,
			"msg": "Order placed"
			}
	else:
		responseObject = {
		"success": False,
		"msg": "Failed to place order"
		}
	return make_response(jsonify(responseObject))


@app.route('/search/id', methods = ['POST'])
@cross_origin()
def searchId():
    data = request.get_json()
    pid = data.get('productId')
    item = get_item_by_id(pid)
    if not item:
        responseObject = {
            "success": False,
            "msg": "no item found for that user id"
        }
    else:
        responseObject = {
            "success": True,
            "item": item
        }
    return make_response(jsonify(responseObject))


@app.route('/orders/id', methods = ['POST'])
@cross_origin()
def get_tracking():
    data = request.get_json()
    oid = data.get('orderId')
    trackingResult = get_tracking_by_order(oid)
    print("tracking result is")
    print(trackingResult)
    if not trackingResult:
        responseObject = {
            "success": False,
            "msg": "no tracking found for that order id"
        }
    else:
        responseObject = {
            "success": True,
            "trackingResult": trackingResult
        }
    return make_response(jsonify(responseObject))


@app.route('/admin', methods = ['POST'])
@cross_origin()
def get_all_inventory():
	data = request.get_json()
	inventory = get_all_items()

	responseObject = {
		"success" : True,
		"inventory" : inventory
	}
	return make_response(jsonify(responseObject))


@app.route('/admin/update', methods = ['POST'])
@cross_origin()
def update_inventory():
	data = request.get_json()
	id = data.get('id')
	quantity = data.get('quantity')
	if admin_update_quantity(id, quantity): 
		responseObject = {
			"success" : True,
			"msg" : "Item quantity successfully updated."
		}
	else:
		responseObject = {
			"success" : False,
			"msg" : "Could not update item quantity. Item may not exist."
		}
	return make_response(jsonify(responseObject))


@app.route('/admin/add', methods = ['POST'])
@cross_origin()
def add_to_inventory():
	data = request.get_json()
	print(data)
	name = data.get('name')
	category = data.get('category')
	desc = data.get('description')
	price = data.get('price')
	stock = data.get('stock')
	weight = data.get('weight')
	w_id = data.get('warehouse_id')
	if not add_item(name, category, desc, price, stock, weight, w_id):
		responseObject = {
			"success" : False,
			"msg" : "could not add item"
		}
	else:
		responseObject = {
			"success" : True,
			"msg" : "added item"
		}
	return make_response(jsonify(responseObject))


if __name__ == '__main__':
    app.run()
    # To view scripts on a different computer on the same network
    # app.run("0.0.0.0", "5010")
