from threading import Thread
from django.views.decorators.csrf import csrf_exempt
from cmath import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson import json_util
import googlemaps

from utils.mongo_connection import orders_collection, restaurant_collection , drivers_collection
from .Simulation import Simulation



city_center =(30.1491, 31.6290)
gkey = 'AIzaSyAv4TshMqyQUcBc_oWM6w9hjlxIKqiUOvA'
gmaps = googlemaps.Client(key= gkey)


# Create your views here.




@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        # Get the request data
        data = json.loads(request.body)
        name = data.get('name')
        details = data.get('details')
        lat = data.get('lat')
        lng = data.get('lng')
        order = {
            "name": name,
            "details": details,
            "lat": lat,
            "lng": lng
        }

        # Insert the order document into the orders collection
        result = orders_collection.insert_one(order)
        if not result.inserted_id:
            return JsonResponse({'error': 'Failed to create order'}, status=500)

        return JsonResponse({'message': 'Order placed successfully', 'order_id': str(result.inserted_id)}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def get_all_orders(request):
    if request.method == 'GET':
        orders_list = list()
        for order in orders_collection.find({}, {'delivery_address': 1, 'status': 1, 'lat': 1, 'lng': 1}):
            try:
                user_result = gmaps.places(query=order.get("delivery_address"), location=city_center, radius=6000)
                user_L= user_result['results'][0]['geometry']['location']
                order["lat"], order["lng"] = user_L['lat'], user_L['lng']
                orders_collection.update_one({"_id": order["_id"]}, {"$set": {"lat": order["lat"],"lng": order["lng"]}})
                orders_list.append(order)
            except:
                pass
            
        orders_json = json.loads(json_util.dumps(orders_list))
        return JsonResponse({'orders': orders_json})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def create_restaurant(request):
    if request.method == 'POST':
        # Get the request data
        data = json.loads(request.body)
        name = data.get('name')
        details = data.get('details')
        lat = data.get('lat')
        lng = data.get('lng')
        restaurant = {
            "name": name,
            "details": details,
            "lat": lat,
            "lng": lng
        }

        # Insert the order document into the restaurant collection
        result = restaurant_collection.insert_one(restaurant)
        if not result.inserted_id:
            return JsonResponse({'error': 'Failed to create restaurant'}, status=500)

        return JsonResponse({'message': 'restaurant placed successfully', 'restaurant_id': str(result.inserted_id)}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



# @csrf_exempt
# def get_all_restaurant(request):
#     if request.method == 'GET':
#         restaurant = list(restaurant_collection.find({}))
#         restaurants_json = json.loads(json_util.dumps(restaurant))
#         return JsonResponse({'restaurants': restaurants_json})
#     else:
#         return JsonResponse({'error': 'Invalid request method.'}, status=405)





@csrf_exempt
def get_all_restaurant(request):
    if request.method == 'GET':
        restaurant_list = list()
        for restaurant in restaurant_collection.find({}, {'name': 1, 'address': 1, 'lat': 1, 'lng': 1, 'icon': 1}):
            try:
                user_result = gmaps.places(query=restaurant.get("address"), location=city_center, radius=6000)
                user_L= user_result['results'][0]['geometry']['location']
                restaurant["lat"], restaurant["lng"] = user_L['lat'], user_L['lng']
                restaurant_collection.update_one({"_id": restaurant["_id"]}, {"$set": {"lat": restaurant["lat"],"lng": restaurant["lng"]}})
                restaurant_list.append(restaurant)
            except:
                pass
        restaurants_json = json.loads(json_util.dumps(restaurant_list))
        return JsonResponse({'restaurants': restaurants_json})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)








@csrf_exempt
def create_driver(request):
    if request.method == 'POST':
        # Get the request data
        data = json.loads(request.body)
        name = data.get('name')
        details = data.get('details')
        lat = data.get('lat')
        lng = data.get('lng')
        driver = {
            "name": name,
            "details": details,
            "lat": lat,
            "lng": lng
        }

        # Insert the driver document into the drivers collection
        result = drivers_collection.insert_one(driver)
        if not result.inserted_id:
            return JsonResponse({'error': 'Failed to create driver'}, status=500)

        return JsonResponse({'message': 'driver placed successfully', 'driver_id': str(result.inserted_id)}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def get_all_drivers(request):
    if request.method == 'GET':
        driver = list(drivers_collection.find({}))
        drivers_json = json.loads(json_util.dumps(driver))
        return JsonResponse({'drivers': drivers_json})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



@csrf_exempt
def start_simulation(request):
    if request.method == 'POST':
        # Get the request data
        data = json.loads(request.body)
        speed_dict = {"S":1, "R":0.1, "F":0.001}
        speed = data.get('speed')
        drivers_number = data.get('drivers_number')
        speed_float = speed_dict.get(speed.upper())
        if not speed_float :
            return JsonResponse({'error': 'speed must be in (S, R, F) choices '}, status=500)



        result = Simulation.start(int(drivers_number), speed_float)

        if not result:
            return JsonResponse({'error': 'Failed to start simulation'}, status=500)

        return JsonResponse({'message': 'simulation started successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def assign_order(request):
    if request.method == 'POST':
        order = Simulation.get_order()
        if not order :
            return JsonResponse({"error": "All Orders Are Assigned"}, status=501)
        
        drivers = Simulation.get_drivers()
        if not drivers :
            return JsonResponse({"error": "No Drivers Available for assigning"}, status=501)

        best_driver, nearest_resturent_location = Simulation._get_best_driver(order, drivers)

        setRedPolyLine = Thread(target=Simulation.assign_order, args=[
            order,
            best_driver,
            nearest_resturent_location
            ])
        
        setRedPolyLine.start()
        order_name = order.get("name")
        driver_name = best_driver.get("name")

        return JsonResponse({"success": f"{order_name}'s Order assigned to driver {driver_name} "}, status=201)


    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


