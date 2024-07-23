from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from rest_framework.views import APIView
from time import sleep
from accounts.models import User
from .forms import CreateConfigForm, ManualCreateConfigForm
from bot_config.forms import SearchConfigForm
from sellers_finance.models import SubSellrsRelation, SellersPrices
from .models import SellersConfigInfo, SellerConfigsEveryServerUsage
from utils import now_timestamp
from .actions import SellersActions
from rest_framework.response import Response


class CreateConfigView(View, LoginRequiredMixin):
    def get(self, request, seller_id):
        seller = User.objects.get(id=seller_id)
        if request.user.level_access == 10:
            form_type = "manual"
            form = ManualCreateConfigForm
        else:
            form_type = "auto"
            form = CreateConfigForm(seller_id=seller_id)
        return render(request, "sellers_create_config.html", {"form": form, "form_type":form_type})

    def post(self, request, seller_id):
        seller = User.objects.get(id=seller_id)
        if request.user.level_access == 10:
            form_type = "manual"
            form = ManualCreateConfigForm(request.POST)
        else:
            form_type = "auto"
            form = CreateConfigForm(request.POST,seller_id=seller_id)

        if form.is_valid():
            ip_limit = 0
            days_limit = 0
            usage_limit = 0
            cd = form.cleaned_data

            if cd['type'] == "limited":
                usage_limit = int(cd["usage_limit"])
                days_limit = int(cd['days_limit'])
            elif cd['type'] == 'usage_unlimit':
                days_limit = int(cd['days_limit'])
                ip_limit = int(cd['ip_limit'])
            elif cd['type'] == 'time_unlimit':
                usage_limit = int(cd["usage_limit"])

            if form_type == 'auto':
                price = SellersPrices.objects.get(usage_limit=usage_limit, expire_limit=days_limit,user_limit=ip_limit).price
            else:
                price = int(cd['price']) * 1000
            if form_type == 'auto':
                days_limit = days_limit * 30
            create_config = SellersActions.create_config(days_limit, usage_limit, ip_limit, price, request.user, seller)
            print(create_config)
            return redirect('sellers_config:config_details', create_config)

        return render(request, 'create_config.html',
                      {'form': form, 'form_type': form_type})


class SearchedConfigsView(View, LoginRequiredMixin):
    def post(self, request):
        form = SearchConfigForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['search_config']
            list_sellers = [request.user, ]
            if request.user.level_access == 1:
                list_sellers.append(
                    seller.child_seller for seller in SubSellrsRelation.objects.filter(parent_seller=request.user))
            list_configs = SellersConfigInfo.objects.filter(Q(name__icontains=text) | Q(uuid__icontains=text),
                                                            seller__in=list_sellers)
            return render(request, "sellers_list_configs_searched.html",
                          {"search_config": form, "configs": list_configs})
        return redirect("accounts:home_sellers")


class ConfigDetailView(View, LoginRequiredMixin):
    def get(self, request, uuid):
        config_infos = SellersConfigInfo.objects.get(uuid=uuid)
        usage = 0
        for us in config_infos.sellerconfigseveryserverusage_set.all():
            usage += us.usage_now
        if not config_infos.start_timestamp:
            started = False
            days_remain = config_infos.days_limit
        else:
            started = True
            days_remain = ((config_infos.start_timestamp + (config_infos.days_limit * 86400)) - now_timestamp()) / 86400

        return render(request, "sellers_config_page.html", {"config_info": config_infos, "usage": usage,
                                                            "days_remain": days_remain, "started": started})


class ListConfigsView(LoginRequiredMixin, View):
    def get(self, request, userid):
        query_string = request.META['QUERY_STRING']
        print(query_string)
        if query_string.startswith("search="):
            searched = query_string.split("search=")[1]
        else:
            searched = False
        print(searched)
        list_configs = []
        if userid == 0:
            configs = SellersConfigInfo.objects.all().order_by("-update", "-name")
        else:
            configs = SellersConfigInfo.objects.filter(seller_id=userid).order_by("-update", "-name")
        now_time = now_timestamp()
        for config in configs:
            if searched:
                if not searched.lower() in config.name.lower() and not searched.lower() in str(config.uuid):
                    continue
            sum_usage = 0
            for usages in config.sellerconfigseveryserverusage_set.all():
                sum_usage += usages.usage_now
            end_usage = False if config.usage_limit == 0 or sum_usage < config.usage_limit else True
            if config.start_timestamp:
                remain = ((config.start_timestamp + (config.days_limit * 86400)) - now_time) / 86400
                expired = True if remain < 0 else False
            else:
                expired = False
                remain = config.days_limit
            list_configs.append({"config": config, "sum_usage": sum_usage, "remain": remain, "expired": expired,
                                 "end_usage": end_usage})
        return render(request, "sellers_list_configs.html",
                      {"list_configs": list_configs, "searched": searched, "userid": userid})

# get prices api _______________________________________________

class ApiGetConfigTimeChoices(APIView):
    def get(self, request):
        sleep(0.25)
        type = request.GET.get('type')
        choices = []
        if type == 'limited':
            obj = SellersPrices.objects.filter(~Q(usage_limit=0) & ~Q(expire_limit=0) & Q(seller=request.user))
            for i in obj:
                if not (i.expire_limit, f"{i.expire_limit} ماه") in choices:
                    choices.append((i.expire_limit, f"{i.expire_limit} ماه"))
        elif type == 'usage_unlimit':
            obj = SellersPrices.objects.filter(Q(usage_limit=0) & ~Q(expire_limit=0) & Q(seller=request.user))
            for i in obj:
                if not (i.expire_limit, f"{i.expire_limit} ماه") in choices:
                    choices.append((i.expire_limit, f"{i.expire_limit} ماه"))
        elif type == 'time_unlimit':
            choices.append((0, '∞'))

        choices = sorted(choices, key=lambda x: x[0])
        return Response({'choices': choices})


class ApiGetConfigUsageChoices(APIView):
    def get(self, request):
        type = request.GET.get('type')
        time = int(request.GET.get('time'))
        choices = []
        if type == 'limited':
            time = time
            obj = SellersPrices.objects.filter(~Q(usage_limit=0) & Q(expire_limit=time) & Q(seller=request.user))
            for i in obj:
                if not (i.usage_limit, f"{i.usage_limit} GB") in choices:
                    choices.append((i.usage_limit, f"{i.usage_limit} GB"))

        elif type == 'usage_unlimit':
            choices.append((0, '∞'))

        elif type == 'time_unlimit':
            obj = SellersPrices.objects.filter(~Q(usage_limit=0) & Q(expire_limit=0) & Q(seller=request.user))
            for i in obj:
                if not (i.usage_limit, f"{i.usage_limit} GB") in choices:
                    choices.append((i.usage_limit, f"{i.usage_limit} GB"))

        choices = sorted(choices, key=lambda x: x[0])
        return Response({'choices': choices})


class ApiGetConfigIPLimitChoices(APIView):
    def get(self, request):
        type = request.GET.get('type')
        time = int(request.GET.get('time'))

        choices = []
        if type == 'limited' or type == 'time_unlimit':
            choices.append((0, '∞'))

        elif type == 'usage_unlimit':
            time = time
            obj = SellersPrices.objects.filter(Q(usage_limit=0) & Q(expire_limit=time) & Q(seller=request.user))
            for i in obj:
                if not (i.user_limit, f"{i.user_limit} کاربره") in choices:
                    choices.append((i.user_limit, f"{i.user_limit} کاربره"))

        choices = sorted(choices, key=lambda x: x[0])
        return Response({'choices': choices})


class ApiGetConfigPriceChoices(APIView):
    def get(self, request):
        time = int(request.GET.get('time'))
        iplimit = int(request.GET.get('iplimit'))
        usage = int(request.GET.get('usage'))
        obj = SellersPrices.objects.get(usage_limit=usage, expire_limit=time, user_limit=iplimit, seller=request.user).price
        return Response({'price': f'{obj:,}'})
