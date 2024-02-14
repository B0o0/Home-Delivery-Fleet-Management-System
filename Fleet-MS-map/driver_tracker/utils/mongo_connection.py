import pymongo
MONGO_DETAILS = "mongodb://localhost:27017"

client = pymongo.MongoClient(MONGO_DETAILS)
database = client['FleetManagementSystem']


orders_collection = database.get_collection("orders")
restaurant_collection = database.get_collection("restaurants")
drivers_collection = database.get_collection("drivers")
sim_collection = database.get_collection("simulation")
