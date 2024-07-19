from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, AddUserForm
from .models import User
from bot_customers.forms import SearchUserForm
from bot_config.forms import SearchConfigForm

# Create your views here.
class LoginView(View):
    formclass = LoginForm
    def get(self, request):
        form = self.formclass
        return render(request, "log_in.html", {"form": form})

    def post(self, request):
        form = self.formclass(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                return redirect("accounts:home_bot")
        return render(request, "log_in.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.error(request, "شما از حساب کاربری خود خارج شدید.")
        return redirect("accounts:login")


class RegisterView(LoginRequiredMixin, View):
    form = AddUserForm
    def get(self, request):
        form = self.form
        return render(request,"register_user.html", {"form": form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User(username=cd["username"], level_access=0,is_active=True)
            user.set_password(cd["password"])
            user.save()
            return redirect("accounts:home_bot")
        return render(request, "register_user.html", {"form": form})


class HomeBotView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.level_access != 10:
                return redirect("accounts:home_sellers")
        else:
            return redirect("accounts:login")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        search_user = SearchUserForm()
        search_config = SearchConfigForm()
        return render(request, "home_bot.html", {"search_user": search_user, "search_config": search_config})


class HomeSellersView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home_sellers.html")
