from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView


class UserLogin(LoginView):
    template_name = 'user/login.html'


class UserLogout(LoginRequiredMixin, LogoutView):
    template_name = 'home.html'
