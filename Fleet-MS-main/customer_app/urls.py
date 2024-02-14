from django.urls import path
from . import views

urlpatterns = [
    path('getCustomer/<str:customer_id>/', views.getCustomer, name='getCustomer'),
    path('login', views.login, name='login'),
    # path('createCustomer', views.createCustomer, name='createCustomer'),
    path('create_new_account', views.create_new_account, name='create_new_account'),
    path('change_password', views.change_password, name='change_password'),
    path('edit_account/<str:customer_id>/', views.edit_account, name='edit_account'),
    path('delete_account/<str:customer_id>/',views.delete_account, name='delete_account'),
    path('view_orders_history/<str:customer_id>/',views.view_orders_history, name='view_orders_history'),
    path('get_product_details/<str:menu_id>/', views.get_product_details,name='get_product_details'),
    path('search_for_restaurant/<str:restaurant_name>/', views.search_for_restaurant,name='search_for_restaurant'),
    path('search_for_market/<str:market_name>/', views.search_for_market, name='search_for_market'),
    path('browse_menus', views.browse_menus, name='browse_menus'),
    path('add_item_to_cart/<str:customer_id>/<str:product_id>/', views.add_item_to_cart, name='add_item_to_cart'),
    path('view_cart', views.view_cart, name='view_cart'),
    path('edit_cart', views.edit_cart, name='edit_cart'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('calculate_cost/<str:delivery_address>/<str:pick_address>/', views.calculate_cost, name='calculate_cost'),
    path('pick_order', views.pick_order, name='pick_order'),
    path('cancel_order/<str:order_id>/', views.cancel_order, name='cancel_order'),
    path('track_order/<str:order_id>/', views.track_order, name='track_order'),
    path('add_order_review', views.add_order_review, name='add_order_review'),
    path('add_business_review', views.add_business_review, name='add_business_review'),

]
