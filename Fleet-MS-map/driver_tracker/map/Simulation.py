
import polyline
import googlemaps
import time
import random
import math
import numpy as np
from .map_socket import sio
import asyncio
from multiprocessing import Process
from .variables import arabic_male_names
from utils.mongo_connection import drivers_collection, orders_collection, restaurant_collection, sim_collection


gkey = 'AIzaSyAv4TshMqyQUcBc_oWM6w9hjlxIKqiUOvA'
gmaps = googlemaps.Client(key=gkey)

class Simulation:
    center_lat = 30.1491
    center_lon = 31.6290
    radius = 6000
    drivers_num = 10
    speed = 0.01
    states = ['busy', 'available', 'not_available']
    drivers_threads = {}
    drivers = []
    drivers_active = {}
    not_available_drivers = {}
    busy_drivers = {}

    @classmethod
    def start(cls, drivers_num, speed):
        cls.drivers_num = drivers_num
        cls.speed = speed
        sim = sim_collection.find_one({})

        if sim :
            sim_collection.update_one({},{"$set":{"sim_status":True}})
        else:
            sim_collection.insert_one({"sim_status":True})
        
        for i in range(1, cls.drivers_num+1):
            driver_num = "driver{}_marker".format(i)
            
            driver_thread_num = "driver{}_thread".format(i)

            driver = cls.generate_random_location()
            driver_val, driver_thread_val = cls.driver_state(driver, i)
            
            cls.drivers.append((driver_num, driver_val))
            cls.drivers_threads[driver_thread_num] = driver_thread_val
        return {"success": "drivers created successfully"}

    #Driver movment before order selection function.
    @classmethod
    def driver_state(cls, driver, num):
        if int(cls.drivers_num/2) > num or cls.drivers_num == 1:
            gen_states = cls.states[1]
        else:
            gen_states = random.choice([cls.states[0], cls.states[2]])
            
        destination = cls.generate_random_location()
        route = cls.create_route(driver, None, destination)
        driver_name = cls.generate_random_name()
        driver_order = cls.generate_random_order(destination, gen_states)
        driver_obj =  cls.create_or_update_driver_db(
            driver_name,
            gen_states,
            driver[0],
            driver[1],
            num,
            driver_order
            )

        if gen_states == cls.states[0]:
            process = Process(target=cls.run_driver, args=(route, driver_obj))
            process.start()
            return driver, None

        elif gen_states == cls.states[1]:
            process = Process(target=cls.socket_send, args=("setActiveDriver", {num:driver_obj}))
            process.start()
            return driver, None
        
        elif gen_states == cls.states[2]:
            process = Process(target=cls.socket_send, args=("setNotAvailableDriver", {num:driver_obj}))
            process.start()
            return driver, None
        
    @classmethod
    def run_driver(cls, route, driver_obj, polyline=None):
        driver_num = driver_obj["number"]
        cls.update_driver_status(driver_num, "busy")
        set_driver = Process(target=cls.socket_send, args=("setBusyDriver",{driver_num:driver_obj}))
        set_driver.start() 
        for j in range(1, len(route)-1):
            location = route[j + 1]
            driver_obj["lat"] = location[0]
            driver_obj["lng"] = location[1]
            setBusyDriver = Process(target=cls.socket_send, args=("setBusyDriver",{driver_num:driver_obj}))
            setBusyDriver.start()
            if polyline :
                if polyline == "red":
                    removePolylineStep = Process(target=cls.socket_send, args=("removeRedPolylineStep",driver_num))
                    removePolylineStep.start()
                    
                else :
                    removePolylineStep = Process(target=cls.socket_send, args=("removeBluePolylineStep",driver_num))
                    removePolylineStep.start()
            time.sleep(cls.speed)
            cls.update_driver_location(driver_num, location[0], location[1])
        next_order = cls.get_driver_next_order(driver_num)
        if polyline :
            if polyline == "red":
                return
        driver_obj = drivers_collection.find_one({"number":driver_num}, {"_id":0})
        if next_order or  driver_obj.get("next_resturent_location"):
            order_location = (next_order["lat"], next_order["lng"])
            driver_location = (driver_obj["lat"], driver_obj["lng"])
            next_resturent_location = driver_obj.get("next_resturent_location")
            next_resturent_location = (next_resturent_location[0], next_resturent_location[1])
            restaurent_route = cls.create_route(driver_location, None, next_resturent_location) 
            next_route = cls.create_route(next_resturent_location, None, order_location)
            driver_obj["next_order"] = {}
            driver_obj["next_resturent_location"] = []
            cls.update_driver(driver_obj)


            setBluePolyLine = Process(target=cls.socket_send, args=("setBluePolyLine", {driver_num:restaurent_route}))
            setBluePolyLine.start()

            setRedPolyLine = Process(target=cls.socket_send, args=("setBluePolyLine", {driver_num:next_route}))
            setRedPolyLine.start()

            removeAvailbleMarker = Process(target=cls.socket_send, args=("removeAvailbleMarker", driver_num))
            removeAvailbleMarker.start()


            cls.run_driver(restaurent_route, driver_obj, polyline="red")
            cls.run_driver(next_route, driver_obj, polyline="blue")

        cls.update_driver_status(driver_num, "available")
        setActiveDriver = Process(target=cls.socket_send, args=("setActiveDriver",{driver_num:driver_obj}))
        setActiveDriver.start()

    @classmethod
    def get_driver_next_order(cls, driver_num):
        document = drivers_collection.find_one({"number": driver_num}, {"_id": 0, "next_order":1})
        next_order = document.get("next_order")
        return next_order

    @classmethod
    def create_or_update_driver_db(cls, name, status, lat, lng, num, order, next_order=[]):
        driver_obj = {
            "name": name,
            "number": num,
            "status": status,
            "lat": lat,
            "lng": lng,
            "order": order,
            "next_order": next_order
        }
        driver = drivers_collection.find_one({"number":num})
        if driver :
            return cls.update_driver(driver_obj)
        return cls.create_driver(driver_obj)
    
    @classmethod
    def create_driver(cls, driver_obj):
        drivers_collection.insert_one(driver_obj)
        driver_obj.pop('_id', None)
        return driver_obj

    @classmethod
    def update_driver(cls, driver_obj):
        drivers_collection.update_one({"number":driver_obj["number"]},{"$set":driver_obj})
        driver_obj.pop('_id', None)
        return driver_obj

    @classmethod
    def update_driver_location(cls, num, lat, lng):
        updated_data = {
            "lat": lat,
            "lng": lng
        }
        drivers_collection.update_one({"number": num}, {'$set': updated_data})

    @classmethod
    def update_driver_status(cls, num, status):
        drivers_collection.update_one({"number": num}, {'$set': {"status": status}})

    @classmethod
    def socket_send(cls, event, args):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_result = loop.run_until_complete(sio.emit(event, args))

    #Function to create a route, takes origin, waypoints and destination as args, and modifies the route to make it more accurate in the simulation, returns list with tuples full of corrdinates for a route.
    @classmethod
    def create_route(cls, orgn, wayp, dest):

        directions_result = gmaps.directions(origin=orgn,
                                            waypoints= wayp,
                                            destination= dest,
                                            mode='driving')
        ply_points = directions_result[0]['overview_polyline']['points']
        route = polyline.decode(ply_points)

        threshold = cls.convert_kmh(40)
        adjusted_route = []

        num_points = len(route)
        
        for i in range(num_points - 1):
            current_coord = route[i]
            next_coord = route[i + 1]
            adjusted_route.append(current_coord)
            
            distance = cls.calculate_distance(current_coord, next_coord)
            
            if distance > threshold:
                num_intermediate_points = math.ceil(distance / threshold)
                x_step = (next_coord[0] - current_coord[0]) / num_intermediate_points
                y_step = (next_coord[1] - current_coord[1]) / num_intermediate_points
                
                for j in range(1, num_intermediate_points):
                    intermediate_x = current_coord[0] + j * x_step
                    intermediate_y = current_coord[1] + j * y_step
                    adjusted_route.append((intermediate_x, intermediate_y))
        
        adjusted_route.append(route[-1]) 
        
        return adjusted_route

    #Convert speeds from KM/H to KM/S
    @classmethod
    def convert_kmh(cls, speed):
        factor = 3600
        conv_speed = speed / factor
        return conv_speed

    #Function to calculate the distance between 2 coords.
    @classmethod
    def calculate_distance(cls, coord1, coord2):
        
        R = 6371.0
        
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        lat1_rad = np.radians(lat1)
        lon1_rad = np.radians(lon1)
        lat2_rad = np.radians(lat2)
        lon2_rad = np.radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c

        return distance
    
    #Function to generate a random location in a given radius.
    @classmethod
    def generate_random_location(cls):
        bearing = np.radians(np.random.uniform(0, 360))
        distance = np.random.uniform(0, cls.radius)

        lat1 = np.radians(cls.center_lat)
        lon1 = np.radians(cls.center_lon)
        lat2 = np.arcsin(np.sin(lat1) * np.cos(distance / 6371000) +
                        np.cos(lat1) * np.sin(distance / 6371000) * np.cos(bearing))
        lon2 = lon1 + np.arctan2(np.sin(bearing) * np.sin(distance / 6371000) * np.cos(lat1),
                                np.cos(distance / 6371000) - np.sin(lat1) * np.sin(lat2))

        lat2 = np.degrees(lat2)
        lon2 = np.degrees(lon2)
        
        return lat2, lon2

    @classmethod
    def generate_random_name(cls):
        first_name = random.choice(arabic_male_names)
        last_name = random.choice(arabic_male_names)
        return first_name + ' ' + last_name

    @classmethod
    def generate_random_order(cls, location, gen_states):
        if gen_states == "busy" : return {
            "address": "random address",
            "detail": "random details",
            "lat": location[0],
            "lng": location[1],
        }
        return {}


    @classmethod
    def get_order(cls):
        query = {"assigned":False}
        projection = {"_id":0}
        order = orders_collection.find_one(query, projection)
        return order

    @classmethod
    def get_drivers(cls):
        drivers = drivers_collection.find({"status":{"$in":["busy", "available"]}},{"_id":0})
        drivers_list = [driver for driver in drivers if not driver.get("next_order", None) ]
        return drivers_list
    
    @classmethod
    def _get_best_driver(cls, order, drivers_list):
        order_location = (order["lat"], order["lng"])
        restaurant_coordinates_list = [(restaurant["lat"], restaurant["lng"]) for restaurant in restaurant_collection.find({},{"_id":0})]
        nearest_resturent_location = cls.get_nearest_location(order_location, restaurant_coordinates_list)
        best_driver = cls.get_best_driver(nearest_resturent_location, drivers_list)
        return best_driver, nearest_resturent_location

    
    @classmethod
    def assign_order(cls, order, best_driver, nearest_resturent_location):
        query = {"assigned":False}
        orders_collection.update_one(query,{"$set":{"assigned":True}})
        order_location = (order["lat"], order["lng"])
        resturent_to_order_route = cls.create_route(nearest_resturent_location, None, order_location)

        if best_driver["status"] == "available":
            best_driver.update({"order":order})
            cls.update_driver(best_driver)
            best_driver_location = (best_driver.get("lat"), best_driver.get("lng"))
            driver_to_resturent_route = cls.create_route(best_driver_location, None, nearest_resturent_location)

            setRedPolyLine = Process(target=cls.socket_send, args=("setRedPolyLine", {best_driver["number"]:driver_to_resturent_route}))
            setRedPolyLine.start()
            
            setBluePolyLine = Process(target=cls.socket_send, args=("setBluePolyLine", {best_driver["number"]:resturent_to_order_route}))
            setBluePolyLine.start()


            removeAvailbleMarker = Process(target=cls.socket_send, args=("removeAvailbleMarker", best_driver["number"]))
            removeAvailbleMarker.start()

            cls.run_driver(driver_to_resturent_route, best_driver, polyline="red")
            cls.run_driver(resturent_to_order_route, best_driver, polyline="blue")
        elif best_driver["status"] == "busy":
            best_driver.update({"next_order":order})
            best_driver.update({"next_resturent_location":nearest_resturent_location})
            cls.update_driver(best_driver)

        return True

    @classmethod
    def get_best_driver(cls, resturent_location, drivers_list):
        best_driver = None
        smalest_time = float('inf')
        for driver in drivers_list:
            if driver["status"] == "busy":
                driver_time = cls.get_busy_driver_time(driver, resturent_location)
            else:
                driver_time = cls.get_available_driver_time(driver, resturent_location)
            if driver_time < smalest_time :
                smalest_time = driver_time
                best_driver = driver
        return best_driver

    @classmethod 
    def get_busy_driver_time(cls, driver, next_destination):
        order = driver.get("order")
        current_destination = (order.get("lat"), order.get("lat"))
        current_location = (driver.get("lat"), driver.get("lng"))
        time_left = cls.get_distance_time(current_location, current_destination)
        time_between_distinations = cls.get_distance_time(current_destination, next_destination)
        return time_left + time_between_distinations
    
    
    @classmethod 
    def get_available_driver_time(cls, driver, destination):
        current_location = (driver.get("lat"), driver.get("lng"))
        time_left = cls.get_distance_time(current_location, destination)
        return time_left


    @classmethod
    def get_nearest_location(cls, location, location_list):
        nearest_location = []
        smalest_time = float('inf')
        for destination in location_list:
            route_time = cls.get_distance_time(location, destination)
            if route_time < smalest_time:
                smalest_time = route_time
                nearest_location = destination
        return nearest_location
            
    @classmethod
    def get_distance_time(cls, location, destination):
        directions_result = gmaps.directions(origin=location,
                                            destination=destination,
                                            mode='driving')

        route_time = directions_result[0]['legs'][0]['duration']['value']
        return route_time
