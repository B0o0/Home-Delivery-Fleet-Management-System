from cmath import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import math
from bson import json_util
from bson.objectid import ObjectId
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
# from utilities.mongodb import *
import pymongo

client = pymongo.MongoClient('mongodb+srv://mostafa:Mo12312300@fleetmanagementsystem.5xv0klr.mongodb.net/test')
dbname = client['FleetManagementSystem']

# Collections
users = dbname["User"]
customers = dbname["Customer"]
drivers = dbname["Driver"]
products = dbname["Item"]
menus = dbname["Menu"]
businesses = dbname["Business"]
orders = dbname["Order"]
business_reviews = dbname["business_reviews"]
vehicles = dbname["Vehicle"]


@csrf_exempt
def add_business(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        business_website = data.get('business_website')
        email = data.get('email')
        address = data.get('address')
        contact_name = data.get('contact_name')
        postal_code = data.get('postal_code')
        business_type = data.get('type')

        # Check if any of the fields are missing
        if not all([name, phone, email, address, contact_name, postal_code, business_type]):
            return JsonResponse({'error': 'Missing fields.'}, status=400)
        
        # Check if the business type is valid
        if business_type not in ['Market', 'Restaurant']:
            return JsonResponse({'error': 'Invalid business type.'}, status=400)
        
        # Check if the business name already exists
        if businesses.find_one({"name": name}):
            return JsonResponse({'error': 'Business with the same name already exists.'}, status=400)
        
        # Create a new menu for the business
        menu = {
            "name": name,
            "items": []
        }
        menu_id = menus.insert_one(menu).inserted_id

        # Create the business document
        business = {
            "name": name,
            "phone": phone,
            "business_website": business_website,
            "email": email,
            "address": address,
            "contact_name": contact_name,
            "postal_code": postal_code,
            "type": business_type,
            "menu": menu_id
        }

        # Insert the business document into the businesses collection
        businesses.insert_one(business)

        return JsonResponse({'message': 'Business added successfully.'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def approve_business(request, user_id):
    if request.method == 'PUT':
        # Find the business document in the users collection
        business = users.find_one({"_id": ObjectId(user_id), "user_type": "business"})

        if not business:
            return JsonResponse({'error': 'Business not found.'}, status=404)

        # Check if the business is already approved
        if business.get('approved', False):
            return JsonResponse({'error': 'Business is already approved.'}, status=400)

        # Update the business document to mark it as approved
        business['approved'] = True

        # Update the business document in the users collection
        users.update_one({"_id": ObjectId(user_id)}, {"$set": business})

        # Create a new menu for the business
        menu = {
            "name": business['name'],
            "items": []
        }
        menu_id = menus.insert_one(menu).inserted_id

        # Insert the menu_id into the business document
        business['menu'] = menu_id

        # Insert the business document into the businesses collection
        businesses.insert_one(business)

        return JsonResponse({'message': 'Business approved and added to the businesses collection.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



@csrf_exempt
def getAllBusiness(request):
    if request.method == 'GET':
        # Get all documents from the 'Business' collection
        data = businesses.find()
        # Convert the MongoDB documents to Python dictionaries and add them to a list
        response_data = [business for business in data]
        # Return the list of dictionaries as a JSON response
        return JsonResponse(json_util.dumps(response_data), safe=False)
    else:
        # Return a 405 error for all other HTTP methods
        return JsonResponse({'error': 'Method not allowed.'}, status=405)


@csrf_exempt
def getAllRestaurant(request):
    if request.method == 'GET':
        # Get all documents from the 'Business' collection with type "Restaurant"
        data = businesses.find({"type": "Restaurant"})
        # Convert the MongoDB documents to Python dictionaries and add them to a list
        response_data = [business for business in data]
        # Return the list of dictionaries as a JSON response
        return JsonResponse(json_util.dumps(response_data), safe=False)
    else:
        # Return a 405 error for all other HTTP methods
        return JsonResponse({'error': 'Method not allowed.'}, status=405)



@csrf_exempt
def getAllMarket(request):
    if request.method == 'GET':
        # Get all documents from the 'Business' collection with type "Market"
        data = businesses.find({"type": "Market"})
        # Convert the MongoDB documents to Python dictionaries and add them to a list
        response_data = [business for business in data]
        # Return the list of dictionaries as a JSON response
        return JsonResponse(json_util.dumps(response_data), safe=False)
    else:
        # Return a 405 error for all other HTTP methods
        return JsonResponse({'error': 'Method not allowed.'}, status=405)



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
        # Get the incoming data from the request
        data = json.loads(request.body)
        # Extract individual fields from the data dictionary
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        address = data.get('address')
        type = data.get('type')
        # Update only the specified fields in the MongoDB collection
        result = businesses.update_one(
            {'_id': ObjectId(business_id)}, {'$set': data})
        # Check if the update was successful
        if result.modified_count == 1:
            return JsonResponse({'message': 'Business updated successfully.'})
        else:
            return JsonResponse({'error': 'Failed to update.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def delete_business(request, business_id):
    if request.method == 'DELETE':
        # Delete the document from the MongoDB collection
        result = businesses.delete_one({'_id': ObjectId(business_id)})
        # Check if the delete was successful
        if result.deleted_count == 1:
            return JsonResponse({'message': 'Business deleted successfully.'})
        else:
            return JsonResponse({'error': 'Failed to delete.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def get_menu(request, id):
    menu = menus.find_one({'_id': ObjectId(id)})
    if not menu:
        business = businesses.find_one({'_id': ObjectId(id)})
        if business:
            menu_id = business.get('menu')
            menu = menus.find_one({'_id': ObjectId(menu_id)})
    if menu:
        menu_name = menu['name']
        item_ids = menu['items']
        menu_items = []
        for item_id in item_ids:
            item = products.find_one({'_id': ObjectId(item_id)})
            if item:
                menu_items.append(item)
        response_data = {
            'menu_name': menu_name,
            'items': menu_items,
        }
        return JsonResponse(response_data, json_dumps_params={'default': json_util.default})
    else:
        response_data = {'error': 'Menu not found'}
        return JsonResponse(response_data, status=404)

@csrf_exempt
def get_all_business_orders(request, business_id):
    if request.method == 'GET':
        order = list(orders.find({"business_id": ObjectId(business_id)}))
        orders_json = json.loads(json_util.dumps(order))
        return JsonResponse({'orders': orders_json})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def get_all_orders(request):
    if request.method == 'GET':
        order = list(orders.find({}))
        orders_json = json.loads(json_util.dumps(order))
        return JsonResponse({'orders': orders_json})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def view_business_reviews(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        business_id = ObjectId(data['business_id'])
        my_business_reviews = []
        for review in business_reviews.find({"business_id": business_id}):
            my_business_reviews.append(review)
        return JsonResponse({"reviews": json_util.dumps(my_business_reviews)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

#view business history
#track orders
#view order details