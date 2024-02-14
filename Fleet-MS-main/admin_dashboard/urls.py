from django.urls import path
from . import views
from . import businessViews
from . import customerViews
from . import driverViews

urlpatterns = [
    
    #business_Views
    path('add_business',businessViews.add_business, name='add_business'),
    path('approve_business/<str:user_id>/',businessViews.approve_business, name='approve_business'),
    path('getAllBusiness',businessViews.getAllBusiness, name='getAllBusiness'),
    path('getAllRestaurant',businessViews.getAllRestaurant, name='getAllRestaurant'),
    path('getAllMarket',businessViews.getAllMarket, name='getAllMarket'),
    path('get_restaurants_orders',businessViews.get_restaurants_orders, name='get_restaurants_orders'),
    path('get_market_orders',businessViews.get_market_orders, name='get_market_orders'),
    path('get_business/<str:business_id>/',businessViews.get_business, name='get_business'),
    path('update_business/<str:business_id>/',businessViews.update_business, name='update_business'),
    path('delete_business/<str:business_id>/',businessViews.delete_business, name='delete_business'),
    path('get_menu/<str:business_id>/',businessViews.get_menu, name='get_menu'),
    path('get_all_business_orders/<str:business_id>/',businessViews.get_all_business_orders, name='get_all_business_orders'),
    path('get_all_orders',businessViews.get_all_orders, name='get_all_orders'),
    path('view_business_reviews',businessViews.view_business_reviews, name='view_business_reviews'),
    
    #customer_Views
    path('get_all_customers',customerViews.get_all_customers, name='get_all_customers'),
    path('getCustomer/<str:customer_id>/',customerViews.getCustomer, name='getCustomer'),
    path('updateCustomer/<str:customer_id>/',customerViews.updateCustomer, name='updateCustomer'),
    path('deleteCustomer/<str:customer_id>/',customerViews.deleteCustomer, name='deleteCustomer'),
    
    #driver_Views
    path('approve_driver/<str:user_id>/',driverViews.approve_driver, name='approve_driver'),
    path('get_vehicle_details/<str:driver_id>/',driverViews.get_vehicle_details, name='get_vehicle_details'), 
    path('getAllDrivers',driverViews.getAllDrivers, name='getAllDrivers'),
    path('getAll_available_Drivers',driverViews.getAll_available_Drivers, name='getAll_available_Drivers'),
    path('getAll_Notavailable_Drivers',driverViews.getAll_Notavailable_Drivers, name='getAll_Notavailable_Drivers'),
    path('getAll_busy_Drivers',driverViews.getAll_busy_Drivers, name='getAll_busy_Drivers'),
    path('view_driver_details/<str:driver_id>/',driverViews.view_driver_details, name='view_driver_details'), 
    path('updateDriver/<str:driver_id>/',driverViews.updateDriver, name='updateDriver'),
    path('deleteDriver/<str:driver_id>/',driverViews.deleteDriver, name='deleteDriver'), 
    
    
    #views
    path('getAllUsers', views.getAllUsers, name='getAllUsers'),
    path('getAll_business_Users', views.getAll_business_Users, name='getAll_business_Users'),
    path('getAll_driver_Users', views.getAll_driver_Users, name='getAll_driver_Users'),
    path('add_admin', views.add_admin, name='add_admin'),
    path('login', views.login, name='login'),
    path('create_new_account', views.create_new_account, name='create_new_account'),
    path('change_password', views.change_password, name='change_password'),
    path('edit_account/<str:user_id>/', views.edit_account, name='edit_account'),
    path('delete_account/<str:user_id>/',views.delete_account, name='delete_account'),
     
     
     
     

    
]