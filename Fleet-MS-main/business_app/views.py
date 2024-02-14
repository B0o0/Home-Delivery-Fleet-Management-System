from cmath import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson import json_util
from bson.objectid import ObjectId
import gridfs
from PIL import Image
import io
import base64
from django.conf import settings
from .udb.mongodb import *
fs = gridfs.GridFS(dbname)




@csrf_exempt
def create_business(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        business_website = data.get('business_website')
        email = data.get('email')
        password = data.get('password')
        address = data.get('address')
        contact_name = data.get('contact_name')
        postal_code = data.get('postal_code')
        business_type = data.get('type')

        # Check if any of the fields are missing
        if not all([name, phone, email,password, address, contact_name, postal_code, business_type]):
            return JsonResponse({'error': 'Missing fields.'}, status=400)
        
        # Check if the business type is valid
        if business_type not in ['Market', 'Restaurant']:
            return JsonResponse({'error': 'Invalid business type. business must be Market or Restaurant '}, status=400)
        
        # Check if the business name already exists
        if businesses.find_one({"name": name}):
            return JsonResponse({'error': 'Business with the same name already exists.'}, status=400)
        
        # Create the business document
        business = {
            "name": name,
            "phone": phone,
            "business_website": business_website,
            "email": email,
            "password": password,
            "address": address,
            "contact_name": contact_name,
            "postal_code": postal_code,
            "type": business_type,
            "user_type": "business"
        }

        # Insert the business document into the users collection
        users.insert_one(business)

        return JsonResponse({'message': 'Business added successfully.'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        business = businesses.find_one({"email": email})
        if business and business['password'] == password:
            # business exists and password matches, return success response
            return JsonResponse({'success': True, 'business_id': str(business['_id']), 'menu_id': str(business['menu']), 'message': 'Login successful'})
        else:
            # business does not exist or password does not match, return error response
            return JsonResponse({'success': False, 'message': 'Invalid email or password'}, status=401)
    else:
        # Invalid request method
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def get_business(request, business_id):
    if request.method == 'GET':
        # Get the document from the MongoDB collection
        business = businesses.find_one({'_id': ObjectId(business_id)})
        if business is None:
            return JsonResponse({'error': 'Business not found.'}, status=404)
        # Convert the ObjectId to a string
        document_dict = dict(business)
        document_dict['id'] = str(document_dict['_id'])
        # Remove the ObjectId from the document
        del document_dict['_id']
        # Return a JSON response with the document data
        return JsonResponse(json_util.dumps(document_dict), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



@csrf_exempt
def update_business(request, business_id):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        updated_business = {}

        # Check if the business exists
        business = businesses.find_one({"_id": ObjectId(business_id)})
        if not business:
            return JsonResponse({'error': 'Business not found.'}, status=404)

        # Update fields that are present in the request data
        if 'name' in data:
            updated_business['name'] = data['name']
        if 'phone' in data:
            updated_business['phone'] = data['phone']
        if 'business_website' in data:
            updated_business['business_website'] = data['business_website']
        if 'email' in data:
            updated_business['email'] = data['email']
        if 'password' in data:
            updated_business['password'] = data['password']
        if 'address' in data:
            updated_business['address'] = data['address']
        if 'contact_name' in data:
            updated_business['contact_name'] = data['contact_name']
        if 'postal_code' in data:
            updated_business['postal_code'] = data['postal_code']
        if 'type' in data:
            # Check if the business type is valid
            if data['type'] not in ['Market', 'Restaurant']:
                return JsonResponse({'error': 'Invalid business type. Business type must be Market or Restaurant.'}, status=400)
            updated_business['type'] = data['type']

        # Perform the update operation
        businesses.update_one({"_id": ObjectId(business_id)}, {"$set": updated_business})

        return JsonResponse({'message': 'Business updated successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



# @csrf_exempt
# def add_item(request):
#     if request.method == 'POST':
#         data = json.loads(request.body) 
#         menu_id = data.get('menu_id')
#         title = data.get('title')
#         price = data.get('price')
#         category = data.get('category')
#         image = data.get('image')
#         description = data.get('description')
#         available = data.get('available')
#         item = {
#             "title": title,
#             "price": price,
#             "category": category,
#             "image": image,
#             "description": description,
#             "available": available,
#         }
#         item_id = items.insert_one(item).inserted_id
#         menus.find_one_and_update({"_id": ObjectId(menu_id)}, {'$push': {'items': item_id}})
#         return JsonResponse({'message': 'Item added successfully'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def get_in_progress_orders(request, business_id):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection with the status "confirmed"
        data = orders.find({"status": "confirmed"})
        # Convert the ObjectId to a string for each document
        response_data = [json.loads(json_util.dumps(doc)) for doc in data]
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def out_for_delivery_orders(request, business_id):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection with the status "In transit"
        data = orders.find({"status": "In transit"})
        # Convert the ObjectId to a string for each document
        response_data = [json.loads(json_util.dumps(doc)) for doc in data]
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def get_completed_orders(request, business_id):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection with the status "delivered"
        data = orders.find({"status": "delivered"})
        # Convert the ObjectId to a string for each document
        response_data = [json.loads(json_util.dumps(doc)) for doc in data]
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def get_orders_price(request, business_id):
    if request.method == 'GET':
        # Get all orders for the specific business
        data = orders.find({"business_id": ObjectId(business_id)})
        
        # Calculate the sum of the total cost
        total_price = sum(order["total_cost"] for order in data)
        
        return JsonResponse({'total_price': total_price}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



# @csrf_exempt
# def get_delivered_orders(request, business_id):
#     if request.method == "GET":
#         # Find delivered orders with the given business ID in the database
#         delivered_orders = orders.find({"business_id": business_id, "status": "pending"})

#         # Convert the orders to a list of dictionaries
#         delivered_orders_list = list(delivered_orders)

#         return JsonResponse(delivered_orders_list, safe=False, json_dumps_params={'default': json_util.default})

#     return JsonResponse({"message": "Invalid request method"}, status=400)


@csrf_exempt
def add_item(request,business_id):
    if request.method == 'POST':
        #data = json.loads(request.body) 
        menu_id = request.POST.get('menu_id')
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')
        description = request.POST.get('description')
        available = request.POST.get('available')
        
        # Get the uploaded image from the request
        image = request.FILES.get('image')
        
        print(image)
        if image:
            # Open the image using PIL and convert it to JPEG format
            img = Image.open(io.BytesIO(image.read()))
            img = img.convert('RGB')
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=95)
            image_binary = output.getvalue()
            
            # Store the image in MongoDB using GridFS
            image_id = fs.put(image_binary, filename=image.name)
            item = {
                "title": title,
                "price": price,
                "category": category,
                "image_id": str(image_id),
                "description": description,
                "available": available,
                'business_id': ObjectId(business_id),
            }
        else:
            item = {
                "title": title,
                "price": price,
                "category": category,
                "description": description,
                "available": available,
                'business_id': ObjectId(business_id),
            }
        
        item_id = items.insert_one(item).inserted_id
        menus.find_one_and_update({"_id": ObjectId(menu_id)}, {'$push': {'items': item_id}})
        return JsonResponse({'message': 'Item added successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
    
    

# @csrf_exempt
# def get_item(request, item_id):
#     if request.method == 'GET':
#         item = items.find_one({"_id": ObjectId(item_id)})

#         if item:
#             image_id = item.get("image_id")
#             if image_id:
#                 # Get the image associated with the item
#                 image = fs.get(ObjectId(image_id)).read()
#                 # Generate the image URL
#                 image_url = f"{settings.BASE_URL}/images/{item_id}"
#                 # Add the image URL to the item document
#                 item["image"] = image_url

#             return JsonResponse(json_util.dumps(item), safe=False)
#         else:
#             return JsonResponse({'error': 'Item not found'})
#     else:
#         return JsonResponse({'error': 'Method not allowed'})
    

@csrf_exempt
def get_item(request, item_id):
    if request.method == 'GET':
        item = items.find_one({"_id": ObjectId(item_id)})
        
        if item:
            image_id = item.get("image_id")
            if image_id:
                # Get the image associated with the item
                image = fs.get(ObjectId(image_id)).read()
                # Convert the image bytes to base64 encoding
                image_base64 = base64.b64encode(image).decode("utf-8")
                # Add the base64-encoded image data to the item document
                item["image"] = image_base64
            
            return JsonResponse(json_util.dumps(item), safe=False)
        else:
            return JsonResponse({'error': 'Item not found'})
    else:
        return JsonResponse({'error': 'Method not allowed'})



@csrf_exempt
def edit_item(request, item_id):
    if request.method == "PATCH":
        data = json.loads(request.body)
        title = data.get("title", None)
        price = data.get("price", None)
        category = data.get("category", None)
        image = data.get("image", None)
        description = data.get("description", None)
        available = data.get("available", None)

        item = items.find_one({"_id": ObjectId(item_id)})
        if not item:
            return JsonResponse({"message": "Item not found"})

        new_item = {
            "title": title or item["title"],
            "price": price or item["price"],
            "category": category or item["category"],
            "image": image or item["image"],
            "description": description or item["description"],
            "available": available or item["available"]
        }

        items.update_one({"_id": ObjectId(item_id)}, {"$set": new_item})
        return JsonResponse({"message": "Item edited successfully"})

    return JsonResponse({"message": "Invalid request method"})


@csrf_exempt
def delete_item(request, menu_id, item_id):
    if request.method == "DELETE":
        item = items.find_one({"_id": ObjectId(item_id)})
        if not item:
            return JsonResponse({"message": "Item not found"})

        menus.update_one({"_id": ObjectId(menu_id)}, {"$pull": {"items": ObjectId(item_id)}})
        items.delete_one({"_id": ObjectId(item_id)})
        return JsonResponse({"message": "Item deleted successfully"})

    return JsonResponse({"message": "Invalid request method"})



@csrf_exempt
def get_current_orders(request, business_id):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection with the status "pending" and specific business_id
        data = orders.find({"status": "pending", "business_id": ObjectId(business_id)})
        # Convert the ObjectId to a string for each document
        response_data = [json.loads(json_util.dumps(doc)) for doc in data]
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def confirm_order(request, order_id):
    if request.method == "POST":
        data = json.loads(request.body)
        # Extract business ID from POST request
        business_id = data.get("business_id")
        if not business_id:
            return JsonResponse({"message": "Business ID missing from request"}, status=400)

        # Find order by ID and check if it's already confirmed
        order = orders.find_one({'_id': ObjectId(order_id)})
        if not order:
            return JsonResponse({"message": "Order not found"}, status=400)
        if order.get('status') == 'confirmed':
            return JsonResponse({"message": "Order already confirmed"}, status=400)

        # Update order status and business status
        orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': 'confirmed', 'business_id': ObjectId(business_id)}})
        return JsonResponse({"message": "Order confirmed successfully"})
    
    return JsonResponse({"message": "Invalid request method"}, status=400)





# def confirm_order(order_id):
#     order = orders.find_one({"_id": ObjectId(order_id)})
#     if not order:
#         return HttpResponse("Order not found.")
#     if order['status'] != 'pending':
#         return HttpResponse("Order has already been confirmed or assigned to a driver.")

#     business_id = order['business_id']
#     assign_order_to_nearest_driver(business_id, order_id)

#     orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": "confirmed"}})

#     return HttpResponse("Order confirmed and assigned to driver.")





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
        if order.get('status') not in ['pending', 'confirmed']:
            return JsonResponse({'error': 'Cannot cancel order'})

        # Update the status and cancellation_reason attributes of the order document
        orders.update_one({'_id': ObjectId(order_id)}, {'$set': {'status': 'cancelled', 'cancellation_reason': cancellation_reason}})

        return JsonResponse({'message': 'Order cancelled successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def get_order_details(request, order_id):
    if request.method == "GET":
        # Find order with given ID in database
        order = orders.find_one({"_id": ObjectId(order_id)})
        if not order:
            return JsonResponse({"message": "Order not found"}, status=404)

        # Extract relevant fields from order document
        order_details = {
            "order_id": str(order["_id"]),
            "customer_id": str(order["customer_id"]),
            "total_cost": order["total_cost"],
            "items": order["items"],
            "status": order["status"],
            "date": order["date"],
            "delivery_address": order["delivery_address"]
        }

        # Convert the MongoDB document to JSON format
        order_details_json = json_util.dumps(order_details)

        return JsonResponse(order_details_json, safe=False)

    return JsonResponse({"message": "Invalid request method"}, status=400)


@csrf_exempt
def view_orders_history(request, business_id):
    if request.method == 'GET':
        # Extract relevant fields from business document
        orders_cursor = dbname["Order"].find({"business_id": ObjectId(business_id)})
        orders = list(orders_cursor)
        orders_details = []
        for order in orders:
            order_details = {
                'order_id': str(order['_id']),
                'customer_id': str(order['customer_id']),
                'total_cost': order['total_cost'],
                'items': order['items'],
                'status': order['status'],
                'date': order['date'],
                'delivery_address': order['delivery_address']
            }
            
            orders_details.append(order_details)
        return JsonResponse({'orders':json_util.dumps (orders_details)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



# @csrf_exempt
# def view_orders_history(request, business_id):
#     if request.method == 'GET':
#         # Extract relevant fields from business document
#         orders_cursor = dbname["Order"].find({"business_id": ObjectId(business_id)})
#         orders = list(orders_cursor)
#         orders_details = []
#         for order in orders:
#             order_details = {
#                 'order_id': str(order['_id']),
#                 'customer_id': str(order['customer_id']),
#                 'total_cost': order['total_cost'],
#                 'items': order['items'],
#                 'status': order['status'],
#                 'date': order['date'],
#                 'delivery_address': order['delivery_address']
#             }
#             orders_details.append(order_details)
#         return JsonResponse(json_util.dumps(orders_details), safe=False)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)






@csrf_exempt
def view_business_reviews(request, business_id):
    if request.method == 'GET':
        my_business_reviews = []
        for review in business_reviews.find({"business_id": ObjectId(business_id)}):
            my_business_reviews.append(review)
        return JsonResponse({"reviews": json_util.dumps(my_business_reviews)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def add_comment_to_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        review_id = ObjectId(data.get('review_id'))
        comment = data.get('comment')

        review = business_reviews.find_one({"_id": review_id})
        # check if the review exists
        if review is None:
            return JsonResponse({"message": "Review not found"}, status=404)

        # add the comment to the review's "comments" list
        comments = review.get("comments", [])
        comments.append(comment)

        # update the review with the new comments list
        business_reviews.update_one({"_id": review_id}, {"$set": {"comments": comments}})
        return JsonResponse({"message": "Comment added successfully"})
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)
    
    
    

