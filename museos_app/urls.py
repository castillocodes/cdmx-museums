from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.signup),
    path('login', views.login),
    path('museum/<int:id>', views.rate),
    path('add_rating', views.add_rating),
    path('signout', views.signout)
]
