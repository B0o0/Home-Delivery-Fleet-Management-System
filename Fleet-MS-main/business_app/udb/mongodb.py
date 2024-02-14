import pymongo


client = pymongo.MongoClient('mongodb+srv://ahmed:2233@fleetmanagementsystem.5xv0klr.mongodb.net/test')
dbname = client['FleetManagementSystem']

# Collections
admins = dbname["Admin"]
users = dbname["User"]
customers = dbname["Customer"]
drivers = dbname["Driver"]
products = dbname["Item"]
items = dbname["Item"]
menus = dbname["Menu"]
businesses = dbname["Business"]
orders = dbname["Order"]
business_reviews = dbname["business_reviews"]
vehicles = dbname["Vehicle"]
business_reviews = dbname["business_reviews"]

