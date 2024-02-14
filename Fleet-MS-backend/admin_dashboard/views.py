from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
from bson import json_util, ObjectId
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import datetime
import pymongo
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


client = pymongo.MongoClient('mongodb+srv://mostafa:Mo12312300@fleetmanagementsystem.5xv0klr.mongodb.net/test')
db = client['FleetManagementSystem']

# Collections
admins = db["Admin"]
users = db["User"]
customers = db["Customer"]
products = db["Item"]
menus = db["Menu"]
businesses = db["Business"]
orders = db["Order"]
business_reviews = db["business_reviews"]


# Create your views here.




@csrf_exempt
def getAllUsers(request):
    if request.method == 'GET':
        # Get all documents from the 'User' collection
        data = users.find()
        # Convert the MongoDB documents to Python dictionaries and add them to a list
        response_data = [user for user in data]
        # Return the list of dictionaries as a JSON response
        return JsonResponse(json_util.dumps(response_data), safe=False)
    else:
        # Return a 405 error for all other HTTP methods
        return JsonResponse({'error': 'Method not allowed.'}, status=405)


@csrf_exempt
def getAll_business_Users(request):
    if request.method == 'GET':
        # Get all user documents with user_type "business" from the 'User' collection
        users = db["User"]
        data = users.find({"user_type": "business"})
        # Convert the MongoDB documents to Python dictionaries and add them to a list
        response_data = [user for user in data]
        # Return the list of dictionaries as a JSON response
        return JsonResponse(json_util.dumps(response_data), safe=False)
    else:
        # Return a 405 error for all other HTTP methods
        return JsonResponse({'error': 'Method not allowed.'}, status=405)


@csrf_exempt
def getAll_driver_Users(request):
    if request.method == 'GET':
        # Get all user documents with user_type "driver" from the 'User' collection
        users = db["User"]
        data = users.find({"user_type": "driver"})
        # Convert the MongoDB documents to Python dictionaries and add them to a list
        response_data = [user for user in data]
        # Return the list of dictionaries as a JSON response
        return JsonResponse(json_util.dumps(response_data), safe=False)
    else:
        # Return a 405 error for all other HTTP methods
        return JsonResponse({'error': 'Method not allowed.'}, status=405)


@csrf_exempt
def add_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        email = data.get('email')
        phone = data.get('phone')
        
        if not username or not password or not confirm_password or not email:
            return JsonResponse({'error': 'Missing required fields'})
        
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'})
        
        existing_admin = admins.find_one({'email': email})
        if existing_admin:
            return JsonResponse({'error': 'An admin with this email already exists'})
        
        # Hash and salt the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        admin_data = {
            'username': username,
            'password': hashed_password.decode('utf-8'),  # Store the hashed password
            'email': email,
            'phone': phone,
            'is_superuser': True,
            'is_staff': True
        }
        
        admins.insert_one(admin_data)
        
        return JsonResponse({'message': 'Admin account created successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})



@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        user = admins.find_one({"email": email})
        if user:
            stored_password = user.get('password')
            # Compare the entered password with the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # Passwords match, authentication successful
                return JsonResponse({'success': True, 'message': 'Login successful'}, status=200)
        
        # User does not exist or password does not match
        return JsonResponse({'success': False, 'message': 'Invalid email or password'}, status=401)



# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         email = data.get('email')
#         password = data.get('password')
#         user = Users.find_one({"email": email, "password": password})
#         if user:
#             # User exists and password matches, redirect to home page
#             return JsonResponse(data, status=200)
#         else:
#             # User does not exist or password does not match, show error message
#             return JsonResponse({'success': False, 'message': 'Invalid email or password'})

@csrf_exempt
def create_new_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        address = data.get('address')
        if users.find_one({"email": email}):
            # User already exists, show error message
            return JsonResponse({'success': False, 'message': 'User with this email already exists'})
        else:
            # Insert the new user and return success response
            user = {
                "name": name,
                "email": email,
                "password": password,
                "phone": phone,
                "address": address,
                "is_verified": False
            }
            result = users.insert_one(user)
            user['_id'] = str(result.inserted_id)
            send_verification_email(request, user)
            return JsonResponse({'success': True, 'message': 'Account created successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


def send_verification_email(request, user):
    # Generate token
    token = default_token_generator.make_token(user)

    # Create verification link
    uidb64 = urlsafe_base64_encode(force_bytes(user['_id']))
    verification_url = request.build_absolute_uri(reverse('verify-account', kwargs={'uidb64': uidb64, 'token': token}))

    # Render email template
    email_subject = 'Verify your account'
    email_body = render_to_string('verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })

    # Send email
    send_mail(email_subject, email_body, None, [user['email']], fail_silently=False)
    return HttpResponse('Verification email sent')


def verify_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = users.find_one({"_id": ObjectId(uid)})
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        # Set user as verified
        result = users.find_one_and_update(
            {"_id": ObjectId(uid)},
            {"$set": {"is_verified": True}},
            return_document=pymongo.ReturnDocument.AFTER
        )
        if result:
            return HttpResponse('Account verified')
        else:
            return HttpResponse('Unable to verify account')
    else:
        return HttpResponse('Invalid verification link')



@csrf_exempt
def change_password(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = users.find_one({"email": email})
        if not user:
            return JsonResponse({'error': 'User with this email does not exist'})
        if user.get('password') != old_password:
            return JsonResponse({'error': 'Old password does not match'})
        users.update_one({"_id": user['_id']}, {"$set": {"password": new_password}})
        return JsonResponse({'message': 'Password updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

# function to edit customer account
# expected to get document with the new data the user want to change from the frontend
# and get the id for the user we want to update
# example new_data = { 'name' : new name, 'password' : new password, etc.... }


@csrf_exempt
def edit_account(request, user_id):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        new_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address
        }
        user = users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return JsonResponse({'error': 'User with this id does not exist'})
        users.update_one({"_id": user['_id']}, {'$set': new_data})
        return JsonResponse({'message': 'Account updated successfully'})
    else:
        user = users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return JsonResponse({'error': 'User with this id does not exist'})
        return JsonResponse(user)


@csrf_exempt
def delete_account(request, user_id):
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return JsonResponse({'error': 'User with this id does not exist'})
    else:
        users.delete_one({"_id": user["_id"]})
        return JsonResponse({'message': 'Account deleted successfully'})