from django.urls import path
from . import views
app_name = 'img'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.img_create, name='img_create'),
    path('images/<int:img_id>/', views.img_detail, name='img_detail'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/', views.follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name="profile_unfollow"
    ),
    path('like/<int:img_id>/', views.img_like, name='img_like'),
]
