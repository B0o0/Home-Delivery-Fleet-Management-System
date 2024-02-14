import pymongo




client = pymongo.MongoClient(
    'mongodb+srv://mostafa:Mo12312300@fleetmanagementsystem.5xv0klr.mongodb.net/test')
db = client['FleetManagementSystem']

# Collections
customers = db["Customer"]
products = db["Item"]
menus = db["Menu"]
businesses = db["Business"]
orders = db["Order"]
business_reviews = db["business_reviews"]