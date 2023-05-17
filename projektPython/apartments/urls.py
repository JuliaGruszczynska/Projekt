from django.urls import path

from apartments import views

urlpatterns = [
    path('', views.hello_word_view, name=''),
    path('favourites/', views.favourites_view, name='favourites'),
    path('add-to-favorites/', views.add_to_favorites, name='add-to-favorites'),

]