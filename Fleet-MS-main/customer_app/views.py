from cmath import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime , timedelta
from .udb.mongodb import *



@csrf_exempt
def getCustomer(request, customer_id):
    if request.method == 'GET':
        # Get the document from the MongoDB collection
        customer = customers.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return JsonResponse({'error': 'Customer not found'})
        # Convert the ObjectId to a string
        document_dict = dict(customer)
        document_dict['id'] = str(document_dict['_id'])
        # Remove the ObjectId from the document
        del document_dict['_id']
        # Return a JSON response with the document data
        return JsonResponse(document_dict, safe=False)
    else:
        return JsonResponse(status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        customer = customers.find_one({"email": email})
        if customer and customer['password'] == password:
            # customer exists and password matches, return success response
            return JsonResponse({'success': True, 'customer_id': str(customer['_id']), 'message': 'Login successful'})
        else:
            # customer does not exist or password does not match, return error response
            return JsonResponse({'success': False, 'message': 'Invalid email or password'}, status=401)
    else:
        # Invalid request method
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def create_new_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        phone = data.get('phone')
        address = data.get('address')
        
        if password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Password and confirm password do not match'}, status=400)
        
        if customers.find_one({"email": email}):
            return JsonResponse({'success': False, 'message': 'User with this email already exists'}, status=400)
        else:
            customer = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "confirm_password": confirm_password,
                "phone": phone,
                "address": address
            }
            result = customers.insert_one(customer)
            return JsonResponse({'success': True, 'id': str(result.inserted_id)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        customer_obj = customers.find_one({"email": email})
        if not customer_obj:
            return JsonResponse({'error': 'User with this email does not exist'})
        if customer_obj.get('password') != old_password:
            return JsonResponse({'error': 'Old password does not match'})
        customers.update_one({"_id": customer_obj['_id']}, {"$set": {"password": new_password}})
        return JsonResponse({'message': 'Password updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# function to edit customer account
# expected to get document with the new data the user want to change from the frontend
# and get the id for the user we want to update
# example new_data = { 'name' : new name, 'password' : new password, etc.... }


@csrf_exempt
def edit_account(request, customer_id):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        new_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "address": address
        }
        customer_obj = customers.find_one({"_id": ObjectId(customer_id)})
        if not customer_obj:
            return JsonResponse({'error': 'User with this ID does not exist'})

        customers.update_one({"_id": customer_obj['_id']}, {'$set': new_data})
        return JsonResponse({'message': 'Account updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)




@csrf_exempt
def delete_account(request, customer_id):
    customer = customers.find_one({"_id": ObjectId(customer_id)})
    if not customer:
        return JsonResponse({'error': 'User with this id does not exist'})
    else:
        customers.delete_one({"_id": customer["_id"]})
        return JsonResponse({'message': 'Account deleted successfully'})




@csrf_exempt
def view_orders_history(request, customer_id):
    if request.method == 'GET':
        customer = customers.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return JsonResponse({'error': 'Invalid customer ID'})

        customer_orders = orders.find({'customer_id': customer_id})
        orders_details = []
        for order in customer_orders:
            order_details = {
                'order_id': str(order['_id']),
                'date': order['date'],
                'total_cost': order.get('total_cost', 0),
                'status': order['status']
            }
            orders_details.append(order_details)

        return JsonResponse({'orders': orders_details})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.core.serializers.json import DjangoJSONEncoder

# @csrf_exempt
# def browse_menus(request):
#     if request.method == 'GET':
#         pipeline = [
#             {
#                 '$lookup': {
#                     'from': 'Item',
#                     'localField': 'items',
#                     'foreignField': '_id',
#                     'as': 'items'
#                 }
#             },
#             {
#                 '$project': {
#                     'items._id': 0,
#                     'items.__v': 0
#                 }
#             }
#         ]

#         menu_list = list(menus.aggregate(pipeline))
#         return JsonResponse({"menu_list": json_util.dumps(menu_list)}, encoder=DjangoJSONEncoder)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def browse_menus(request):
    if request.method == 'GET':
        menu_list = []
        for menu in menus.find():
            menu_data = json_util.loads(json_util.dumps(menu))
            item_list = []
            for item_id in menu_data['items']:
                item = products.find_one({"_id": ObjectId(item_id)})
                if item:
                    item_data = json_util.loads(json_util.dumps(item))
                    item_list.append(item_data)
            menu_data['items'] = item_list
            menu_list.append(menu_data)
        return JsonResponse({"menu_list": json_util.dumps(menu_list)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



# @csrf_exempt
# def browse_menus(request):
#     if request.method == 'GET':
#         menu_list = []
#         for menu in menus.find():
#             menu_list.append(json_util.loads(json_util.dumps(menu)))
#         return JsonResponse({"menu_list": json_util.dumps(menu_list)})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_product_details(request, menu_id):
    # find the menu with the given ID
    menu = menus.find_one({"_id": ObjectId(menu_id)})

    # get the product IDs for the menu
    product_ids = menu["items"]

    # get the products for the menu by querying the "products" collection
    products_details = []
    for product_id in product_ids:
        product = products.find_one({"_id": ObjectId(product_id)})
        products_details.append(product)

    # convert the list of MongoDB documents to a list of dictionaries
    products_dict = json.loads(json_util.dumps(products_details))

    # return the list of dictionaries as a JSON response
    return JsonResponse(products_dict, safe=False)


def search_for_restaurant(request, restaurant_name):

    restaurant = businesses.find_one(
        {"name": restaurant_name, "type": "restaurant"})
    restaurant = json.loads(json_util.dumps(restaurant))
    if not restaurant:
        return JsonResponse({'message': 'No restaurant found with the given name.'})
    else:
     return JsonResponse(restaurant, safe=False)


def search_for_market(request, market_name):
    market = businesses.find_one({"name": market_name, "type": "market"})
    market = json.loads(json_util.dumps(market))
    if not market:
        return JsonResponse({'message': 'No market found with the given name.'})

    return JsonResponse(market, safe=False)




@csrf_exempt
def add_item_to_cart(request, customer_id, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_quantity = int(data.get('product_quantity'))
            
            # Find the customer document with the given customer ID
            customer = customers.find_one({'_id': ObjectId(customer_id)})
            if not customer:
                return JsonResponse({'success': False, 'error': 'Invalid customer ID'})
            
            # Find the product document with the given ID
            product = products.find_one({'_id': ObjectId(product_id)})
            if not product:
                return JsonResponse({'success': False, 'error': 'Invalid product ID'})
            
            # Add the item details to the customer's cart
            cart = customer.get('cart', [])
            cart_item = {
                'product_id': product_id,
                'product_name': product.get('title'),
                'quantity': product_quantity,
                'business_id': product.get('business_id')
            }
            if cart_item not in cart:
                cart.append(cart_item)
            
            # Update the customer's cart
            customers.update_one({'_id': ObjectId(customer_id)}, {'$set': {'cart': cart}})
            
            return JsonResponse({'success': True, 'message': 'Item added to cart'})
        except (ValueError, TypeError) as e:
            return JsonResponse({'success': False, 'error': 'Invalid request data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)




def edit_cart(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        cart_items = request.POST.get('cart_items')

        # Convert the cart items JSON string to a list of dictionaries
        cart_items = json.loads(cart_items)

        customer = customers.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return JsonResponse({'success': False})

        # Update the cart items
        cart = customer.get('cart', [])
        for item in cart_items:
            product_id = item['product_id']
            quantity = item['quantity']
            # If quantity is 0, remove the cart item
            if quantity == 0:
                cart = [x for x in cart if x['product_id']
                        != ObjectId(product_id)]
            else:
                # Otherwise, update the quantity of the cart item
                cart_item = next(
                    (x for x in cart if x['product_id'] == ObjectId(product_id)), None)
                if cart_item:
                    cart_item['quantity'] = quantity
                else:
                    cart_item = {'product_id': ObjectId(
                        product_id), 'quantity': quantity}
                    cart.append(cart_item)

            # Update the cart item in the database
            customer.update_one({'_id': customer['_id'], 'cart.product_id': ObjectId(product_id)},
                                {'$set': {'cart.$.quantity': quantity},
                                    '$setOnInsert': {'cart.$': cart_item}},
                                upsert=True)

        # Update the user's cart in the database
        customer.update_one({'_id': customer['_id']}, {'$set': {'cart': cart}})

        return JsonResponse({'success': True})


def view_cart(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        if not customer_id:
            return JsonResponse({'success': False, 'error': 'No customer_id provided'})

        # Find the customer document with the given customer_id
        customer = customers.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return JsonResponse({'success': False, 'error': 'Customer not found'})

        # Get the cart items
        cart = customer.get('cart', [])

        # Get the product details for each cart item
        products_details = []
        for item in cart:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            if product_id:
                product = products.find_one({'_id': ObjectId(product_id)})
                if product:
                    products_details.append({
                        'product_id': str(product_id),
                        'title': product.get('title'),
                        'price': product.get('price'),
                        'description': product.get('description'),
                        'category': product.get('category'),
                        'quantity': quantity
                    })

        return JsonResponse(products_details, safe=False)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def clear_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        customer = customers.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return JsonResponse({'success': False, 'message': 'Customer not found'})

        # clear the cart for this customer
        customers.update_one({'_id': customer['_id']}, {'$set': {'cart': []}})

        return JsonResponse({'success': True, 'message': 'Cart cleared successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

# order status
# pending: The order has been received but has not yet been confirmed.
# Confirmed: The order has been confirmed and is being processed.
# In transit: The order has been shipped or is being delivered.
# Delivered: The order has been delivered to the customer.
# Cancelled: The order has been cancelled by either the customer or the business.
# Refunded: The order has been refunded due to an issue with the product or service.
# On hold: The order is temporarily on hold, usually due to an issue with payment or a product being out of stock.


@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        # Get the customer ID from the request POST data
        data = json.loads(request.body)
        customer_id = data.get('customer_id')

        # Find the user document with the given customer ID
        customer = customers.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return JsonResponse({'error': 'Invalid customer ID'})

        # Get the cart items
        cart = customer.get('cart', [])

        # Calculate the total cost of the order
        cost = 0
        business_id = None
        for item in cart:
            product_id = item['product_id']
            quantity = item['quantity']
            business_id = item["business_id"]
            product = products.find_one({'_id': ObjectId(product_id)})
            if product:
                cost += quantity * float(product['price'])

        # Get the pickup address from the business
        business = businesses.find_one({"_id": ObjectId(business_id)})
        if not business:
            return JsonResponse({'error': 'Invalid business ID'})
        pickup_address = business.get("address")

        # Check if the customer has provided a delivery address
        delivery_address = customer.get('address')
        if not delivery_address:
            # Prompt the user to provide a delivery address
            return JsonResponse({'error': 'Please provide a delivery address'})

        delivery_cost = calculate_cost(delivery_address, pickup_address)
        total_cost = cost + delivery_cost

        # Get the current date and time
        now = datetime.now()

        # Calculate the expected delivery time
        delivery_time = now + timedelta(hours=1)  # Assuming a delivery time of 1 hour from the current time

        # Create an order document
        order = {
            'customer_id': customer_id,
            'items': cart,
            'status': 'pending',
            'date': now.strftime('%Y-%m-%d %H:%M:%S'),
            'delivery_address': delivery_address,
            'pickup_address': pickup_address,
            'cost': cost,
            'delivery_cost': delivery_cost,
            'total_cost': total_cost,
            'expected_delivery_time': delivery_time.strftime('%Y-%m-%d %H:%M:%S'),
            'business_id': business_id,
            'ordered_from':'Restaurant'
        }

        # Insert the order document into the orders collection
        result = orders.insert_one(order)
        if not result.inserted_id:
            return JsonResponse({'error': 'Failed to place order'})

        # Clear the user's cart
        customers.update_one({'_id': ObjectId(customer_id)}, {'$set': {'cart': []}})

        return JsonResponse({'message': 'Order placed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)





def calculate_cost(delivery_address, pick_address):
    # Use Google Maps Directions API to get the route distance and duration with traffic for car driving
    api_key = 'AIzaSyAv4TshMqyQUcBc_oWM6w9hjlxIKqiUOvA'
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={pick_address}&destination={delivery_address}&mode=driving&departure_time=now&traffic_model=best_guess&key={api_key}'
    response = requests.get(url)
    data = response.json()

    # Check if the API request was successful
    if data['status'] != 'OK':
        raise Exception('Failed to retrieve route information from Google Maps')

    # Extract the distance in meters and convert it to kilometers
    distance = data['routes'][0]['legs'][0]['distance']['value'] / 1000

    # Calculate the cost based on the distance (assuming a rate of $5 per kilometer)
    cost = distance * 5
    return cost



# pick_order function : used if customer want to get order from external business that's not in our database
# it need to get delivery_address and pick_address and description of what the customer want
# and the cost can be calculeted by the function calculate_cost assuming that the cost of 1 km is 5 pounds

@csrf_exempt
def pick_order(request):
    if request.method == 'POST':
        try:
            # Get the request data
            data = json.loads(request.body)
            customer_id = data['customer_id']
            description = data['description']
            delivery_address = data['delivery_address']
            pick_address = data['pick_address']
            
            # Find the user document with the given customer_id
            customer = customers.find_one({'_id': ObjectId(customer_id)})
            if not customer:
                return JsonResponse({'error': 'Customer not found'}, status=404)

            # Get the current date and time
            now = datetime.now()
            
            # Calculate the expected delivery time (1 hour from the current time)
            expected_delivery_time = now + timedelta(hours=1)
            
            cost = calculate_cost(delivery_address, pick_address)
            
            # Create an order document
            order = {
                'customer_id': customer_id,
                'description': description,
                'status': 'In transit',
                'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                'delivery_address': delivery_address,
                'pick_address': pick_address,
                'delivery_cost': cost,
                'expected_delivery_time': expected_delivery_time.strftime('%Y-%m-%d %H:%M:%S'),
                'ordered_from':'Market'
            }

            # Insert the order document into the orders collection
            result = orders.insert_one(order)
            if not result.inserted_id:
                return JsonResponse({'error': 'Failed to create order'}, status=500)

            return JsonResponse({'message': 'Order placed successfully', 'order_id': str(result.inserted_id)}, status=201)


        except KeyError:
            return JsonResponse({'error': 'Invalid request data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
def cancel_order(request, order_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Get the cancellation reason from the request POST data
        cancellation_reason = data.get('cancellation_reason')

        # Find the order document with the given ID
        order = orders.find_one({'_id': ObjectId(order_id)})
        if not order:
            return JsonResponse({'error': 'Invalid order ID'})

        # Check if the order can be cancelled
        if order.get('status') not in ['pending']:
            return JsonResponse({'error': 'Cannot cancel order'})

        # Update the status and cancellation_reason attributes of the order document
        orders.update_one({'_id': ObjectId(order_id)}, { '$set': {'status': 'cancelled', 'cancellation_reason': cancellation_reason}})

        return JsonResponse({'message': 'Order cancelled successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



def track_order(request, order_id):
    # Find the order document with the given ID
    order = orders.find_one({'_id': ObjectId(order_id)})
    if not order:
        return HttpResponse('Invalid order ID')

    # Check if the order is in transit
    if order.get('status') != 'in transit':
        return HttpResponse('Order is not in transit')

    # Get the delivery address from the order document
    delivery_address = order.get('delivery_address')

    # you need to covert the delivery location and the driver current location to latitude and longitude
    # then you need to view both on the map (all of this by google maps api)
    # This code returns a simple response with the map location
    return HttpResponse('Map location')


# def track_order(request, order_id):
#     # Find the order document with the given ID
#     order = orders.find_one({'_id': ObjectId(order_id)})
#     if not order:
#         return JsonResponse({'error': 'Invalid order ID'})

#     # Check if the order is in transit
#     if order.get('status') != 'in transit':
#         return JsonResponse({'error': 'Order is not in transit'})

#     # Get the delivery address from the order document
#     delivery_address = order.get('delivery_address')

#     # Obtain the latitude and longitude of the delivery address using the Google Geocoding API
#     geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={delivery_address}&key=YOUR_API_KEY'
#     response = requests.get(geocoding_url)
#     if response.status_code != 200:
#         return JsonResponse({'error': 'Failed to retrieve geolocation data'})

#     geocoding_data = response.json()
#     if geocoding_data['status'] != 'OK' or len(geocoding_data['results']) == 0:
#         return JsonResponse({'error': 'Failed to retrieve geolocation data'})

#     location = geocoding_data['results'][0]['geometry']['location']
#     delivery_latitude = location['lat']
#     delivery_longitude = location['lng']

#     # Obtain the driver's current location (assuming you have access to it)
#     driver_latitude = 37.7749
#     driver_longitude = -122.4194

#     # Prepare the response data
#     response_data = {
#         'delivery_address': delivery_address,
#         'delivery_latitude': delivery_latitude,
#         'delivery_longitude': delivery_longitude,
#         'driver_latitude': driver_latitude,
#         'driver_longitude': driver_longitude,
#     }

#     # Return the JSON response
#     return JsonResponse(response_data)


@csrf_exempt
def add_order_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = ObjectId(data['order_id'])
        feedback = data['feedback']
        rating = int(data['rating'])
        delivery_person_rating = int(data['delivery_person_rating'])
        delivery_person_feedback = data['delivery_person_feedback']

        order = orders.find_one({'_id': order_id})
        if not order:
            return JsonResponse({'success': False, 'message': 'Order not found'})

        # Check if the order has been delivered
        if order.get('status') != 'delivered':
            return JsonResponse({'success': False, 'message': 'Order has not been delivered yet'})
        

        # Update the delivery_review attribute of the order document
        orders.update_one(
            {'_id': order_id},
            {'$set': {
                'rating': rating,
                'feedback': feedback,
                'delivery_person_rating': delivery_person_rating,
                'delivery_person_feedback': delivery_person_feedback
            }}
        )
        return JsonResponse({'success': True, 'message': 'Review added successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def add_business_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_id = ObjectId(data['customer_id'])
        business_id = ObjectId(data['business_id'])
        review_text = data['review_text']
        rating = int(data['rating'])

        business = businesses.find_one({'_id': business_id})
        if not business:
            return JsonResponse({'success': False, 'message': 'Business not found'})

        business_review = {
            'business_id': business_id,
            'review_text': review_text,
            'rating': rating,
            'customer_id': customer_id,
            'created_at': datetime.now()
        }
        business_reviews.insert_one(business_review)
        return JsonResponse({'success': True, 'message': 'Review added successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

# @csrf_exempt
# def browse_menus(request):
#     if request.method == 'GET':
#         data = json.loads(request.body)
#         # Get the menu_id parameter from the query string
#         menu_id = data.get('menu_id')

#         # Retrieve the menus based on the menu_id parameter
#         if menu_id:
#             menu = menus.find_one({'_id': ObjectId(menu_id)})
#             if menu:
#                 return JsonResponse(json.loads(json_util.dumps(menu)))
#             else:
#                 return HttpResponse(status=404)
#         else:
#             menu_list = []
#             for menu in menus.find():
#                 menu_list.append(json.loads(json_util.dumps(menu)))
#             return JsonResponse({'menu_list': menu_list}, safe=False)

#browse menus


