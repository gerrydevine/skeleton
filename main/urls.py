from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
]

# Adding urls for User Auth
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
