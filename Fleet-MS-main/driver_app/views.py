from cmath import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson import json_util
from bson.objectid import ObjectId
from .udb.mongodb import *


# driver status
# Not available : driver can view orders but can not accept orders
# Available : driver can accept orders
# busy : driver accepted order and order is In transit and driver can not be "Not available"




@csrf_exempt
def create_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        licence_id = data.get('licence_id')
        email = data.get('email')
        password = data.get('password')
        address = data.get('address')
        

        # Check if any of the fields are missing
        if not all([first_name, last_name, phone, licence_id, email, address, password]):
            return JsonResponse({'error': 'Missing fields.'}, status=400)

        # Create the driver document
        driver = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "licence_id": licence_id,
            "email": email,
            "password": password,
            "address": address,
            "user_type": "driver"
        }

        # Insert the driver document into the users collection
        users.insert_one(driver)

        return JsonResponse({'message': 'Driver created successfully.'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)






@csrf_exempt
def add_vehicle(request, driver_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        vehicle_plat_id = data['vehicle_plat_id']
        model = data['model']
        year = data['year']
        color = data['color']
        license_date = data['license_date']

        # Check if driver already has a vehicle
        existing_vehicle = vehicles.find_one({"driver_id": driver_id})
        if existing_vehicle:
            return JsonResponse({'error': 'Driver already has a vehicle'}, status=400)

        # Insert new vehicle to the collection
        vehicle = {
            "vehicle_plat_id": vehicle_plat_id,
            "model": model,
            "year": year,
            "color": color,
            "license_date": license_date,
            "driver_id": driver_id
        }
        vehicle_id = vehicles.insert_one(vehicle).inserted_id

        # Update driver with new vehicle information
        driver = drivers.find_one({"_id": ObjectId(driver_id)})
        if driver:
            driver_vehicles = driver.get("vehicles", [])
            driver_vehicles.append(str(vehicle_id))
            drivers.update_one({"_id": ObjectId(driver_id)}, {"$set": {"vehicles": driver_vehicles}})

            return JsonResponse({'success': 'Vehicle added successfully'})
        else:
            return JsonResponse({'error': 'Driver not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def update_vehicle(request, driver_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        vehicle_plat_id = data['vehicle_plat_id']
        model = data['model']
        year = data['year']
        color = data['color']
        license_date = data['license_date']

        # Find the vehicle associated with the driver ID
        vehicle = vehicles.find_one({"driver_id": driver_id})
        if vehicle:
            vehicle_id = str(vehicle['_id'])

            # Update vehicle in the collection
            updated_vehicle = {
                "vehicle_plat_id": vehicle_plat_id,
                "model": model,
                "year": year,
                "color": color,
                "license_date": license_date,
                "driver_id": driver_id
            }
            vehicles.update_one({"_id": ObjectId(vehicle_id)}, {"$set": updated_vehicle})

            return JsonResponse({'success': 'Vehicle updated successfully'})
        else:
            return JsonResponse({'error': 'Vehicle not found for the given driver'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def change_status(request, driver_id):
    if request.method == 'POST':
        driver = drivers.find_one({"_id": ObjectId(driver_id)})
        if driver:
            status = driver.get("status")
            if status == "Not available":
                drivers.update_one({"_id": ObjectId(driver_id)}, {"$set": {"status": "available"}})
                return JsonResponse({"status": "success"})
            elif status == "available" or status != "busy":
                drivers.update_one({"_id": ObjectId(driver_id)}, {"$set": {"status": "Not available"}})
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "driver is busy with an order"}, status=400)
        else:
            return JsonResponse({"status": "error", "message": "Driver not found"}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@csrf_exempt
def view_orders(request):
    if request.method == 'GET':
        orders_list = []
        for order in orders.find({"status": "confirmed"}):
            orders_list.append(order)
        return JsonResponse({'orders': json_util.dumps(orders_list)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def view_delivery_address(request, order_id):
    if request.method == 'GET':
        order = orders.find_one({"_id": ObjectId(order_id)})
        if order:
            delivery_address = order.get("delivery_address")
            return JsonResponse({'delivery_address': json_util.dumps(delivery_address)})
        else:
            return JsonResponse({'error': 'Order not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def accept_order(request, driver_id, order_id):
    if request.method == 'POST':
        order = orders.find_one({"_id": ObjectId(order_id)})
        if order and order.get("status") == "confirmed":
            driver = drivers.find_one({"_id": ObjectId(driver_id)})
            if driver and driver.get("status") == "available":
                orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": "in_transit", "driver_id": driver_id}})
                drivers.update_one({'_id': ObjectId(driver_id)},{'$set': {'status': 'busy'}})
                return JsonResponse({"status": "success", "order": json_util.dumps(order)})
            else:
                return JsonResponse({"status": "error", "message": "Driver not found or not available"}, status=404)
        else:
            return JsonResponse({"status": "error", "message": "Order not found or not confirmed"}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@csrf_exempt
def order_delivered(request, driver_id, order_id):
    if request.method == 'POST':
        order = orders.find_one({"_id": ObjectId(order_id)})
        if order and order.get("status") == "In transit":
            orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": "delivered", "driver_id": driver_id}})
            drivers.update_one({'_id': ObjectId(driver_id)}, {'$set': {'status': 'available'}})
            return JsonResponse({"status": "success", "order": json_util.dumps(order)})
        else:
            return JsonResponse({"status": "error", "message": "Order not found or not in transit"}, status=404)
        
        
