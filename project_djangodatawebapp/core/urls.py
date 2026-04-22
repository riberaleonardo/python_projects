from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("records/", views.record_list, name="record_list"),
    path("records/add/", views.record_add, name="record_add"),
    path("records/<int:pk>/", views.record_detail, name="record_detail"),
    path("records/<int:pk>/edit/", views.record_edit, name="record_edit"),
    path("records/<int:pk>/delete/", views.record_delete, name="record_delete"),
    path("fetch/", views.fetch_data_view, name="fetch_data_view"),
]