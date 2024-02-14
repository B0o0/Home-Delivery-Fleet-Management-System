import pymongo
MONGO_DETAILS = 'mongodb+srv://ahmed:2233@fleetmanagementsystem.5xv0klr.mongodb.net/test'

client = pymongo.MongoClient(MONGO_DETAILS)
dbname = client['FleetManagementSystem']


orders_collection = dbname.get_collection("Order")
restaurant_collection = dbname.get_collection("Business")
drivers_collection = dbname.get_collection("drivers")
sim_collection = dbname.get_collection("simulation")
