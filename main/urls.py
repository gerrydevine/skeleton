from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('records/', include('records.urls')),
]

# # Adding urls for User Auth
# urlpatterns += [
# ]
