#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
from django.urls import path
import records.views as views


urlpatterns = [
    path('', views.RecordListView.as_view(), name='record-list'),
    # path('create/', views.RecordCreateView.as_view(), name='record-create'),
    path('create/', views.record_create_view, name='record-create'),
    # path('<int:pk>', views.RecordDetailView.as_view(), name='record-view'),
    path('search/', views.record_search_view, name='record-search'),
    path('<int:pk>', views.record_detail_view, name='record-details'),
    path('<int:pk>/update/', views.RecordUpdateView.as_view(), name='record-update'),
    path('<int:pk>/delete/', views.RecordDeleteView.as_view(), name='record-delete'),
]