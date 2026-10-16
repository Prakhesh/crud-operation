from django.urls import path
from . import views

urlpatterns = [
    path("Register/", views.register),
    path("Login/", views.user_login),
    path("Create/", views.create),
    path("Read/", views.read),
    path("Update/<int:id>/", views.update),
    path("Delete/<int:id>/", views.delete),
    path("Logout/", views.user_logout),
]