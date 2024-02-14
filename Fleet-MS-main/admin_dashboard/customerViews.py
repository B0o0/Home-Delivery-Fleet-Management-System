from cmath import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from .udb.mongodb import *



# @csrf_exempt
# def get_all_customers(request):
#     if request.method == 'GET':
#         # Get the document from the MongoDB collection
#         data = customers.find()
#         response_data = []
#         for customer in data:
#             # Convert the ObjectId to a string
#             customer['_id'] = str(customer['_id'])
#             # add the document to the response data list
#             response_data.append(customer)
#         return JsonResponse(response_data, safe=False)
#     else:
#         return JsonResponse(status=405)


@csrf_exempt
def get_all_customers(request):
    if request.method == 'GET':
        # Get the documents from the MongoDB collection
        data = list(customers.find())
        response_data = []
        for customer in data:
            # Convert the ObjectId to a string
            customer['_id'] = str(customer['_id'])
            # add the document to the response data list
            response_data.append(customer)
        return JsonResponse(json_util.dumps(response_data), safe=False)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)



@csrf_exempt
def getCustomer(request, customer_id):
    if request.method == 'GET':
        # Get the document from the MongoDB collection
        customer = customers.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return JsonResponse({'error': 'Customer not found'})
        # Convert the ObjectId to a string
        document_dict = dict(customer)
        document_dict['id'] = str(document_dict['_id'])
        # Remove the ObjectId from the document
        del document_dict['_id']
        # Return a JSON response with the document data
        return JsonResponse(dumps(document_dict), safe=False)
    else:
        return JsonResponse(status=405)

@csrf_exempt
def updateCustomer(request, customer_id):
    if request.method == 'PATCH':
        # Get the incoming data from the request
        data = json.loads(request.body)
        # Update the document in the MongoDB collection
        result = customers.update_one({'_id': ObjectId(customer_id)}, {'$set': data})
        if result.modified_count == 0:
            # No documents were modified, return an error response
            return JsonResponse({'error': 'Customer not found'}, status=404)
        # Return a JSON response with a success message
        return JsonResponse({'message': 'Customer updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



@csrf_exempt
def deleteCustomer(request, customer_id):
    if request.method == 'DELETE':
        customer = customers.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return JsonResponse({'error': 'Customer not found'})        
        # Delete the customer document from the MongoDB collection
        customer = customers.delete_one({'_id': ObjectId(customer_id)})
        # Return a JSON response with the deleted customer ID
        return JsonResponse({'messege': "Customer deleted successfully"})
    else:
        return JsonResponse(status=405)



