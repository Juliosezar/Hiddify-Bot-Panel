from django.shortcuts import render, redirect
from .models import Server
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import AddServerForm, EditServerForm

class ShowServers(LoginRequiredMixin, View):
    def get(self, request):
        obj = Server.objects.all()
        return render(request, "show_servers.html", {'servers': obj})


class AddServer(LoginRequiredMixin, View):
    def get(self, request):
        form = AddServerForm()
        return render(request, "add_server.html", {'form': form})

    def post(self, request):
        form = AddServerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Server.objects.create(
                ID=cd["ID"],
                name=cd["name"],
                proxy_path=cd["proxy_path"],
                port=cd["port"],
                server_domain=cd["server_domain"],
                fake_domain=cd["fake_domain"],
                admin_uuid=cd["admin_uuid"],
                sellers_sub_uuid=cd["sellers_sub_uuid"],
                bot_sub_uuid=cd["bot_sub_uuid"],
                active=cd["active"],
                old_iphone=cd["old_iphone"]
            ).save()
            return redirect('servers:show_servers')
        return render(request, "add_server.html", {'form': form})



class EditServer(LoginRequiredMixin, View):
    def get(self, request, server_id):
        form = EditServerForm(server_id=server_id)
        return render(request, "add_server.html", {'form': form})

    def post(self, request, server_id):
        form = EditServerForm(request.POST, server_id=server_id)
        if form.is_valid():
            cd = form.cleaned_data
            obj = Server.objects.get(server_id=server_id)
            obj.name = cd["name"]
            obj.proxy_path = cd["proxy_path"]
            obj.port = cd["port"]
            obj.server_domain = cd["server_domain"]
            obj.fake_domain = cd["fake_domain"]
            obj.admin_uuid = cd["admin_uuid"]
            obj.sellers_sub_uuid = cd["sellers_sub_uuid"]
            obj.bot_sub_uuid = cd["bot_sub_uuid"]
            obj.active = cd["active"]
            obj.old_iphone = cd["old_iphone"]
            obj.save()
            return redirect('servers:show_servers')
        return render(request, "add_server.html", {'form': form, "edit": True})
