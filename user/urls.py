from django.urls import path

from . import views as user_views

app_name = 'user'
urlpatterns = [
    path('login/', user_views.UserLogin.as_view(), name='login'),
    path('logout/', user_views.UserLogout.as_view(), name='logout'),
]
