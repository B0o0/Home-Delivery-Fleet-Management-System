from django.urls import path
from . import views

urlpatterns = [
    
path('create_driver', views.create_driver, name='create_driver'),    
path('add_vehicle/<str:driver_id>/', views.add_vehicle, name='add_vehicle'),
path('update_vehicle/<str:driver_id>/', views.update_vehicle, name='update_vehicle'),
path('change_status/<str:driver_id>/', views.change_status, name='change_status'),    
path('view_orders', views.view_orders, name='view_orders'),
path('view_delivery_address/<str:order_id>/', views.view_delivery_address, name='view_delivery_address'),
path('accept_order/<str:driver_id>/<str:order_id>/', views.accept_order, name='accept_order'),
path('order_delivered/<str:driver_id>/<str:order_id>/', views.order_delivered, name='order_delivered'),
    
    
    
]