from django.urls import include, path

urlpatterns = [
  #  path('mongo_auth/', include('mongo_auth.urls')),
    path('admin/', include("admin_dashboard.urls")),
    path('customer/', include("customer_app.urls")),
    path('business/', include("business_app.urls")),
    path('driver/', include("driver_app.urls")),
]

