from django.conf import settings
from pymongo import MongoClient

def get_mongo_client():
    client = MongoClient('mongodb+srv://mostafa:Mo12312300@fleetmanagementsystem.5xv0klr.mongodb.net/')
    return client['FleetManagementSystem']