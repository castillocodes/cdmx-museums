from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.signup),
    path('login', views.login),
    path('museum/<int:id>', views.rate),
    path('add_rating/<int:id>', views.add_rating),
    path('signout', views.signout),
    path('rate-feed', views.add_rating),
    path('dashboard', views.dashboard)
]