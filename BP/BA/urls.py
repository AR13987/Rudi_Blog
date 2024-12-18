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
    path('profile/', views.profile_view, name='profile')
]