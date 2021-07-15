from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.signup),
    path('login', views.login),
    path('museum/<int:id>', views.rate),
    path('add_rating/<int:id>', views.add_rating),
    path('signout', views.signout),
    path('rate-feed', views.rate_feed),
    path('dashboard', views.dashboard),
    path('your-ratings', views.contributions),
    path('edit-rating-opinion/<int:id>', views.edit_rating_opinion),
    path('rating/delete/<int:id>', views.delete_rating),
    path('modify_edit_opinion/<int:id>', views.modify_edit_opinion),
]