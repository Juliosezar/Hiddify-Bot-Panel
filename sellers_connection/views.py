from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import NewBotForm
from .models import Bots

class bots_list(LoginRequiredMixin, View):
    def get(self, request):
        form = NewBotForm()
        model_obj = Bots.objects.all()
        return render(request, "bots_list.html", {"form": form, "model_obj": model_obj})

    def post(self, request):
        model_obj = Bots.objects.all()
        form = NewBotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sellers_connection:list_bots")
        return render(request, "bots_list.html", {"form": form, "model_obj": model_obj})
