from django.urls import path
from . import views

urlpatterns = [
    
    path('create_business', views.create_business, name='create_business'),
    path('login', views.login, name='login'),
    path('get_business/<str:business_id>/', views.get_business, name='get_business'),
    path('update_business/<str:business_id>/', views.update_business, name='update_business'),
    path('get_in_progress_orders/<str:business_id>/', views.get_in_progress_orders, name='get_in_progress_orders'),
    path('out_for_delivery_orders/<str:business_id>/', views.out_for_delivery_orders, name='out_for_delivery_orders'),
    path('get_completed_orders/<str:business_id>/', views.get_completed_orders, name='get_completed_orders'),
    path('get_orders_price/<str:business_id>/', views.get_orders_price, name='get_orders_price'),
    # path('get_delivered_orders/<str:business_id>/', views.get_delivered_orders, name='get_delivered_orders'),
    path('add_item/<str:business_id>/', views.add_item, name='add_item'),
    path('get_item/<str:item_id>/', views.get_item, name='get_item'),
    path('edit_item/<str:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item/<str:menu_id>/<str:item_id>/', views.delete_item, name='delete_item'),
    path('get_current_orders/<str:business_id>/', views.get_current_orders, name='get_current_orders'),
    path('confirm_order/<str:order_id>/', views.confirm_order, name='confirm_order'),
    path('cancel_order/<str:order_id>/', views.cancel_order, name='cancel_order'),
    path('get_order_details/<str:order_id>/', views.get_order_details, name='get_order_details'),
    path('view_orders_history/<str:business_id>/', views.view_orders_history, name='view_orders_history'),
    path('view_business_reviews/<str:business_id>/', views.view_business_reviews, name='view_business_reviews'),
    path('add_comment_to_review', views.add_comment_to_review, name='add_comment_to_review'),
    
    
]
