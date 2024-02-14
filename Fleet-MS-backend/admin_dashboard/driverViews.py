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
def approve_driver(request, user_id):
    if request.method == 'PUT':
        # Find the driver document in the users collection
        driver = users.find_one({"_id": ObjectId(user_id), "user_type": "driver"})

        if not driver:
            return JsonResponse({'error': 'Driver not found.'}, status=404)

        # Check if the driver is already approved
        if driver.get('approved', False):
            return JsonResponse({'error': 'Driver is already approved.'}, status=400)

        # Update the driver document to mark it as approved
        driver['approved'] = True
        driver['approved_at'] = datetime.utcnow().isoformat()
        
        # Update the driver document in the users collection
        users.update_one({"_id": ObjectId(user_id)}, {"$set": driver})

        # Add the user_id to the driver document
        driver['user_id'] = user_id
        driver['status'] = 'available'

        # Insert the driver document into the drivers collection
        drivers.insert_one(driver)

        return JsonResponse({'message': 'Driver approved.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)





# @csrf_exempt
# def approve_driver(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         email = data.get('email')
#         driver = drivers.find_one({"email": email})
#         if driver:
#             # Driver already exists, show error message
#             return JsonResponse({'success': False, 'message': 'Driver with this email already exists'})
#         else:
#             # Insert the new driver and redirect to home page
#             user = users.find_one({"email": email})
#             if user:
#                 driver_data = {
#                     'user_id': str(user.get('_id')),
#                     'name': user.get('name'),
#                     'email': email,
#                     'phone': user.get('phone'),
#                     "approved_at": datetime.now(),
#                     'status': 'available'
#                 }

#                 # Insert driver data into MongoDB
#                 driver_id = drivers.insert_one(driver_data).inserted_id

#                 # Update user collection with driver ID
#                 users.update_one({"_id": user.get('_id')}, {"$set": {"driver_id": str(driver_id)}})

#                 return JsonResponse({'message': 'Driver created successfully', 'id': str(driver_id)})
#             else:
#                 # User with this email not found, show error message
#                 return JsonResponse({'success': False, 'message': 'User with this email not found'})
#     else:
#         return HttpResponse('Invalid request method.')


@csrf_exempt
def create_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return HttpResponse("Email is required to create a driver.")

        # Check if email exists in the User collection
        user = users.find_one({"email": email})
        if not user:
            return HttpResponse(f"No user found with email: {email}")
        driver = drivers.find_one({"email": email})
        if driver:
            return HttpResponse(f"driver with this email already exist: {email}")

        # Retrieve location and get latitude and longitude
        location = data.get('location')
        if not location:
            return HttpResponse("Location is required to create a driver.")
        try:
            response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key=<AIzaSyAv4TshMqyQUcBc_oWM6w9hjlxIKqiUOvA>')
            result = response.json()['results'][0]['geometry']['location']
            latitude = result['lat']
            longitude = result['lng']
        except:
            return HttpResponse("Failed to retrieve latitude and longitude for the given location.")

        # Create dictionary object with driver information
        driver_data = {
            'user_id': str(user.get('_id')),
            'name': user.get('name'),
            'email': email,
            'phone': user.get('phone'),
            'latitude': latitude,
            'longitude': longitude,
            'status': 'available'
        }

        # Insert driver data into MongoDB
        driver_id = drivers.insert_one(driver_data).inserted_id

        # Update user collection with driver ID
        users.update_one({"_id": user.get('_id')}, {"$set": {"driver_id": str(driver_id)}})

        return HttpResponse('Driver created successfully.')
    else:
        return HttpResponse('Invalid request method.')


def get_vehicle_details(request, driver_id):
    vehicle = vehicles.find_one({'driver_id': driver_id})
    if vehicle:
        vehicle['_id'] = str(vehicle['_id'])
        return JsonResponse(vehicle, json_dumps_params={'default': json_util.default})
    else:
        return HttpResponse('Vehicle not found.')



@csrf_exempt
def getAllDrivers(request):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection
        data = drivers.find()
        # Convert the ObjectId to a string for each document
        response_data = [json.loads(json_util.dumps(doc)) for doc in data]
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def getAll_available_Drivers(request):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection with the status "available"
        data = drivers.find({"status": "available"})
        # Convert the ObjectId to a string for each document
        response_data = [json.loads(json_util.dumps(doc)) for doc in data]
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def getAll_Notavailable_Drivers(request):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection with the status "Not available"
        data = drivers.find({"status": "Not available"})
        # Convert the ObjectId to a string for each document
        response_data = [json.loads(json_util.dumps(doc)) for doc in data]
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def getAll_busy_Drivers(request):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection with the status "busy"
        data = drivers.find({"status": "busy"})
        # Convert the ObjectId to a string for each document
        response_data = [json.loads(json_util.dumps(doc)) for doc in data]
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def view_driver_details(request, driver_id):
    if request.method == 'GET':
        # Get the document from the MongoDB collection
        driver = drivers.find_one({'_id': ObjectId(driver_id)})
        if not driver:
            return JsonResponse({'error': 'Driver not found'}, status=404)
        # Convert the ObjectId to a string
        document_dict = dict(driver)
        document_dict['id'] = str(document_dict['_id'])
        # Remove the ObjectId from the document
        del document_dict['_id']
        # Return a JSON response with the document data
        return JsonResponse(json_util.dumps(document_dict), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def updateDriver(request, driver_id):
    if request.method == 'PATCH':
        # Get the incoming data from the request
        data = json.loads(request.body)
        # Update the document in the MongoDB collection
        result = drivers.update_one({'_id': ObjectId(driver_id)}, {'$set': data})
        if result.modified_count == 0:
            # No documents were modified, return an error response
            return JsonResponse({'error': 'Driver not found'}, status=404)
        # Return a JSON response with a success message
        return JsonResponse({'message': 'Driver updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def deleteDriver(request, driver_id):
    if request.method == 'DELETE':
        driver = drivers.find_one({'_id': ObjectId(driver_id)})
        if not driver:
            return JsonResponse({'error': 'Driver not found'})        
        # Delete the driver document from the MongoDB collection
        driver = drivers.delete_one({'_id': ObjectId(driver_id)})
        # Return a JSON response with the deleted driver ID
        return JsonResponse({'messege': "Driver deleted successfully"})
    else:
        return JsonResponse(status=405)


#track drivers    