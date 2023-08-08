#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
from django.urls import path
import records.views as views


urlpatterns = [
    path('', views.record_list_view, name='record-list'),
    path('create/', views.record_create_view, name='record-create'),
    path('search/', views.record_search_view, name='record-search'),
    path('<int:pk>', views.record_detail_view, name='record-details'),
    path('<int:pk>/update/', views.record_update_view, name='record-update'),
    path('<int:pk>/delete/', views.record_delete_view, name='record-delete'),
]