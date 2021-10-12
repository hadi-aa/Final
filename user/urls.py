from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views as user_views

app_name = 'user'
urlpatterns = [
    path('login/', user_views.UserLogin.as_view(), name='login'),
    path('logout/', user_views.UserLogout.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
