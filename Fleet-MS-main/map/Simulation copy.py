
from ipyleaflet import Map, Marker,Icon,AwesomeIcon, Polyline, WidgetControl
from ipywidgets import HTML
import polyline
import googlemaps
import time
import random
import threading
import math
import numpy as np

#Declaring variables.
city_center =(30.1491, 31.6290)
gkey = 'AIzaSyAv4TshMqyQUcBc_oWM6w9hjlxIKqiUOvA'
gmaps = googlemaps.Client(key= gkey)
user_L_input = input("Please enter your location here:")
user_result = gmaps.places(query=user_L_input, location=city_center, radius=6000)
user_L= user_result['results'][0]['geometry']['location']
user_Location= (user_L['lat'], user_L['lng'])
t = None
res1_L = (30.169933760292054, 31.60212133655109)
res2_L = (30.151048942124014, 31.604312550213006)
res3_L = (30.137025464418745, 31.613309996237213)
states = ['Moving', 'Idle']
drivers_active = []
drivers_idle = []
drivers_threads = {}

#Map initialization.
m = Map(center=user_Location, zoom=13)


#Function to generate a random location in a given radius.


def generate_random_location(center_lat, center_lon, radius):
    
    bearing = np.radians(np.random.uniform(0, 360))
    distance = np.random.uniform(0, radius)

    lat1 = np.radians(center_lat)
    lon1 = np.radians(center_lon)
    lat2 = np.arcsin(np.sin(lat1) * np.cos(distance / 6371000) +
                     np.cos(lat1) * np.sin(distance / 6371000) * np.cos(bearing))
    lon2 = lon1 + np.arctan2(np.sin(bearing) * np.sin(distance / 6371000) * np.cos(lat1),
                             np.cos(distance / 6371000) - np.sin(lat1) * np.sin(lat2))

    lat2 = np.degrees(lat2)
    lon2 = np.degrees(lon2)
    
    return lat2, lon2

#Convert speeds from KM/H to KM/S
def convert_kmh(speed):
    factor = 3600
    conv_speed = speed / factor
    return conv_speed


#Function that runs the driver on a randomly generated route, driver moves until an order is given.
class Driver_Thread(threading.Thread):

    def __init__(self, drivermarker):
        super().__init__()
        self.stop_event = threading.Event()
        self.drivermarker = drivermarker

    def run(self):
            try:
                new_location = generate_random_location(city_center[0], city_center[1], 6000)
                route = create_route(self.drivermarker.location, None, new_location)
                self.drivermarker.location = new_location

                for j in range(1, len(route)-1):    
                    self.drivermarker.location = route[j + 1]
                    time.sleep(t)
                    if self.stop_event.is_set():
                        break

            except AttributeError:
                pass

    def stop(self):
        self.stop_event.set()
    

#Function to create a route, takes origin, waypoints and destination as args, and modifies the route to make it more accurate in the simulation, returns list with tuples full of corrdinates for a route.
def create_route(orgn, wayp, dest):

    directions_result = gmaps.directions(origin=orgn,
                                         waypoints= wayp,
                                         destination= dest,
                                         mode='driving')
    ply_points = directions_result[0]['overview_polyline']['points']
    route = polyline.decode(ply_points)

    threshold = convert_kmh(40)
    adjusted_route = []

    num_points = len(route)
    
    for i in range(num_points - 1):
        current_coord = route[i]
        next_coord = route[i + 1]
        adjusted_route.append(current_coord)
        
        distance = calculate_distance(current_coord, next_coord)
        
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

#Function to add a marker
def add_marker(loc, color):
    marker = Marker(location = loc,
                    draggable = False,)
    marker.icon = AwesomeIcon(name='bicycle',
                              marker_color="lightred",
                              icon_color=color)
    m.add_layer(marker)
    return marker

#Function to calculate the distance between 2 coords.
def calculate_distance(coord1, coord2):
    
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


#Selecting simulation speed (driver movment speed)
while True:
  print('Select test speed: S (Slow), R (Real-time), F (Fast)')
  s = input()
  if s=='S' or s=='s':
    t = 10
    print('You chose "Slow"')
    break
  elif s=='R' or s=='r':
    t = 1
    print('You chose "Real-time"')
    break
  elif s=='F' or s=='f':
    t = 0.1
    print('You chose "Fast"')
    break
  else:
    print("Invalid choice.")
    continue


#Restaurant 1 Marker settings and initialization.
res1_icon = Icon(icon_url='https://static.slickdealscdn.com/attachment/1/8/6/3/2/3/2/9853645.attach',
                 icon_size=[50, 30])
res1 = Marker(location=res1_L,
              icon= res1_icon,
              draggable = False,
              title ="MacDonald's")

msg_res1 = HTML()
msg_res1.value= "<h1> MacDonland's</h1><img src='https://lh5.googleusercontent.com/p/AF1QipN9x9DTbTqFV50Q1h7swwCSscrOoQQKysZ4ulRF=w408-h306-k-no' width= 400px> <p> Fast food restaurant. </p>"

m.add_layer(res1)
res1.popup=msg_res1

#Restaurant 2 Marker setting and initialization.
res2_icon = Icon(icon_url = 'https://cdn.iconscout.com/icon/free/png-256/free-kfc-2-226243.png',
                 icon_size=[36,36])
res2 = Marker(location=res2_L,
              icon=res2_icon,
              draggable = False,
              title ='KFC')

msg_res2 = HTML()
msg_res2.value= "<h1> KFC</h1><img src='https://lh5.googleusercontent.com/p/AF1QipN_zggGY9K6sMcG6oOhHBUbOyDSu6Np1nLPwHvX=w426-h240-k-no' width= 800x> <p> Fried Chicken fast food restaurant. <p>"

m.add_layer(res2)
res2.popup=msg_res2

#Restaurant 3 Marker setting and initialization.
res3_icon= Icon(icon_url='https://play-lh.googleusercontent.com/xru00DAxwfDcnP2qv5vX_uX_cPRuh3XUNSW47kBrGKU8HwW3em8MOCQZLHR2TLGK-lM',
                icon_size= [35,35])
res3 = Marker(location=res3_L,
              icon=res3_icon,
              draggable = False,
              title ="Papa John's")

msg_res3 = HTML()
msg_res3.value= "<h1> Papa John's Pizza </h1><img src='https://lh5.googleusercontent.com/p/AF1QipOO9jNEjuD6oCLZI2t0pYcLIPm8f0NW7ZUALGkH=w408-h288-k-no' width= 800px height= 600px> <p> Pizza Restaurant </p>"

m.add_layer(res3)
res3.popup=msg_res3

#User Location
user_tracker = Marker(location=user_Location,
                 draggable = False)

user_tracker.icon = AwesomeIcon(name='user',
                           marker_color='green',
                           icon_color='black')
m.add_layer(user_tracker)


#Driver movment before order selection function.
def driver_state():
     gen_states = random.choice(states)

     if gen_states == states[0]:
          driverL = generate_random_location(city_center[0], city_center[1], 6000)
          driver = add_marker(driverL, 'lightgreen')
          drivers_active.append(driver)
          driver_th = Driver_Thread(drivermarker=driver)
          driver_th.start()
          
          return driver, driver_th

     elif gen_states == states[1]:
          driverL = generate_random_location(city_center[0], city_center[1], 6000)
          driver = add_marker(driverL, 'yellow')
          drivers_idle.append(driver)
          return driver, None

#Generating a desired amount of drivers.
while True:
    num_drivers = int(input('Enter the amount of drivers you want in the simulation: '))
    if isinstance(num_drivers, int) and num_drivers <= 50:
        break
    else:
        print("Input value is incorrect or value is larger than 50, please try again.")
        continue

drivers = []
for i in range(num_drivers+1):
    driver_num = "driver{}_marker".format(i)
    
    driver_thread_num = "driver{}_thread".format(i)

    driver_val, driver_thread_val = driver_state()
    
    drivers.append((driver_num, driver_val))
    drivers_threads[driver_thread_num] = driver_thread_val


#Function to select the route the user wants to see.
print("Choose an option:")
print('1. Route 1 to "MacDonalds"')
print('2. Route 2 to "KFC"')
print('3. Route 3 to "Papa Johns"')

def res_select(choice):
 while True:

   if choice == "1":
    selected = res1_L
    print("You chose Option 1.")
    return selected

   elif choice == "2":
    selected = res2_L
    print("You chose Option 2.")
    return selected

   elif choice == "3":
    selected = res3_L
    print("You chose Option 3.")
    return selected

   else:
    print("Invalid choice.")
    continue


selected_res = res_select(input("Enter your choice (1-3): "))

#Calculate fastest driver to do the order.
fastest_route_time = float('inf')
fastest_driver = None

for driver in drivers_active:
    directions_result = gmaps.directions(origin=driver.location,
                                         destination=selected_res,
                                         mode='driving')

    route_time = directions_result[0]['legs'][0]['duration']['value']

    if route_time < fastest_route_time:
        fastest_route_time = route_time
        fastest_driver = driver

for index, tuple_value in enumerate(drivers):
    if tuple_value[1] == fastest_driver:
           d_thread = drivers_threads.get('driver{}_thread'.format(index))
            
d_thread.stop()


#Move marker method
def move_marker(selected_driver):
 
 route_1 = create_route(selected_driver.location, None, selected_res)
 route_2 = create_route(selected_res, None, user_Location)

#Polylines
 polyline_1 = Polyline(locations=route_1, color='#6495ED', weight=5, fill=False)
 m.add_layer(polyline_1)

 polyline_2 = Polyline(locations=route_2, color='#DC143C', weight=5, fill=False)
 m.add_layer(polyline_2)

#Moving the Marker
 start_time = time.time()
 for i in range(1, len(route_1)-1):
     selected_driver.location = route_1[i+1]
     time.sleep(t)

 m.remove_layer(polyline_1)

 for j in range(1, len(route_2)-1):
      selected_driver.location = route_2[j+1]
      time.sleep(t)

 m.remove_layer(polyline_2)

 end_time = time.time()
 time_lapsed = end_time - start_time

 return time_lapsed


def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Test Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))



time_convert(move_marker(fastest_driver))

print("\nTest Completed!")



