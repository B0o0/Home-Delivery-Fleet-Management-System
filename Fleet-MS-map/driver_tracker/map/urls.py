from .views import *


from django.urls import path


urlpatterns = [
    
    #business_Views
    path('create_order', create_order, name='create_order'),
    path('get_all_orders', get_all_orders, name='get_all_orders'),

    path('create_restaurant', create_restaurant, name='create_restaurant'),
    path('get_all_restaurant', get_all_restaurant, name='get_all_restaurant'),

    path('create_driver', create_driver, name='create_driver'),
    path('get_all_drivers', get_all_drivers, name='get_all_drivers'),


    path('start_simulation', start_simulation, name='start_simulation'),
    path('assign_order', assign_order, name='assign_order'),

    ]