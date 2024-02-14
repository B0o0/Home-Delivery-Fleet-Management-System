from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  #  path('mongo_auth/', include('mongo_auth.urls')),
    path('super/', admin.site.urls ),
    path('admin/', include("admin_dashboard.urls")),
    path('customer/', include("customer_app.urls")),
    path('business/', include("business_app.urls")),
    path('driver/', include("driver_app.urls")),
    path('map/', include('map.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)