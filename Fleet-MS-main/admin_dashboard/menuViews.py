import pymongo
from bson import ObjectId

client = pymongo.MongoClient('mongodb+srv://mostafa:Mo12312300@fleetmanagementsystem.5xv0klr.mongodb.net/test')
dbname = client['FleetManagementSystem']
item = dbname["Item"]
menu = dbname["Menu"]


# menu.aggregate([{"$lookup": {"from": "Item", "localField": "items", "foreignField": "_id", "as": "items"}}]).next()


def get_menu(menu_id):
    itemsIds = []
    items = []
    menu1 = menu.find_one({"_id": menu_id})
    itemsIds = menu1.get('items')
    menuName = menu1.get('name')
    for i in range(len(itemsIds)):
        items.append(item.find_one({"_id": itemsIds[i]}))
    return menuName, items


# test

menuId = input("enter menu id : ")
menuId = ObjectId(menuId)
print(get_menu(menuId))
