from django.urls import path
from . import views
app_name = 'BA'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]

urlpatterns += [
    path('editing_profile/', views.editing_profile_view, name='editing_profile'),
    path('profile/', views.profile_view, name='profile'),
    path('delete_profile/', views.delete_profile_view, name='delete_profile'),
]

urlpatterns += [
    path('create_post/', views.create_post_view, name='create_post'),
    path('like_post/<int:post_id>/', views.like_post_view, name='like_post'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]