from django.shortcuts import render,redirect
from bot_finance.models import Prices
from bot_config.actions import BotAction
from servers.models import Server
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from time import sleep
from django.db.models import Q
from .forms import CreateConfigForm, ManualCreateConfigForm
from .models import BotConfigInfo, BotConfigsEveryServerUsage
from utils import now_timestamp
from django.contrib import messages
from .forms import SearchConfigForm

class BotCreateConfigView(LoginRequiredMixin, View):
    def get(self, request, form_type):
        forms = {'auto': CreateConfigForm, 'manual': ManualCreateConfigForm}
        return render(request, 'create_config.html',
                      {'form': forms[form_type],
                       'form_type': form_type})

    def post(self, request, form_type):
        forms = {'auto': CreateConfigForm, 'manual': ManualCreateConfigForm}
        form = forms[form_type](request.POST)
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
                price = Prices.objects.get(usage_limit=usage_limit, expire_limit=days_limit, user_limit=ip_limit).price
            else:
                price = cd['price']
            paid = cd["paid"]
            if form_type == 'auto':
                days_limit = days_limit * 30
            create_config = BotAction.create_config_by_admins(days_limit, usage_limit, ip_limit, price, paid, request.user.username),
            print(create_config)
            return redirect('bot_config:config_page',create_config[0])


        return render(request, 'create_config.html',
                      {'form': form, 'form_type': form_type})


class ConfigPageView(LoginRequiredMixin, View):
    def get(self, request, config_uuid):
        config_infos = BotConfigInfo.objects.get(uuid=config_uuid)
        usage = 0
        for us in BotConfigsEveryServerUsage.objects.filter(config__uuid=config_uuid):
            usage += us.usage_now
        if not config_infos.start_timestamp:
            started = False
            days_remain = config_infos.days_limit
        else:
            started = True
            days_remain = ((config_infos.start_timestamp + (config_infos.days_limit * 86400)) - now_timestamp()) / 86400

        return render(request, "config_page.html", {"config_info": config_infos, "usage": usage,
                        "days_remain": days_remain, "started":started})


class ListConfigsSearched(LoginRequiredMixin, View):
    def post(self, request):
        form = SearchConfigForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data["search_config"]
            model_obj = BotConfigInfo.objects.filter(Q(name__icontains=word) | Q(uuid__icontains=word))
            if not model_obj.exists():
                messages.error(request, 'کانفیگی با این مشخصات یافت نشد.')
            return render(request, "list_configs_searched.html",
                          {"configs_model": reversed(model_obj), "search_config": form})
        return redirect('accounts:home_bot')


class ConfigsListView(ListConfigsSearched, View):

    def get(self, request, *args, **kwargs):
        query_string = request.META['QUERY_STRING']
        if query_string.startswith("search="):
            searched = query_string.split("search=")[1]
        else:
            searched = False
        print(searched)
        list_configs = []
        configs = BotConfigInfo.objects.all()
        now_time = now_timestamp()
        for config in configs:
            if searched:
                if not searched.lower() in config.name.lower() and not searched.lower() in str(config.uuid):
                    continue
            sum_usage = 0
            for usages in config.botconfigseveryserverusage_set.all():
                sum_usage += usages.usage_now
            end_usage = False if config.usage_limit == 0 or sum_usage < config.usage_limit else True
            if config.start_timestamp:
                remain = ((config.start_timestamp + (config.days_limit * 86400)) - now_time) / 86400
                expired = True if remain < 0 else False
            else:
                expired = False
                remain = config.days_limit
            list_configs.append({"config":config, "sum_usage": sum_usage, "remain": remain, "expired": expired, "end_usage":end_usage})
        return render(request, "list_configs.html", {"list_configs": list_configs, "searched":searched})






# create config by admin api
class ApiGetConfigTimeChoices(APIView):
    def get(self, request):
        sleep(0.25)
        type = request.GET.get('type')
        choices = []
        if type == 'limited':
            obj = Prices.objects.filter(~Q(usage_limit=0) & ~Q(expire_limit=0))
            for i in obj:
                if not (i.expire_limit, f"{i.expire_limit} ماه") in choices:
                    choices.append((i.expire_limit, f"{i.expire_limit} ماه"))
        elif type == 'usage_unlimit':
            obj = Prices.objects.filter(Q(usage_limit=0) & ~Q(expire_limit=0))
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
            obj = Prices.objects.filter(~Q(usage_limit=0) & Q(expire_limit=time))
            for i in obj:
                if not (i.usage_limit, f"{i.usage_limit} GB") in choices:
                    choices.append((i.usage_limit, f"{i.usage_limit} GB"))

        elif type == 'usage_unlimit':
            choices.append((0, '∞'))

        elif type == 'time_unlimit':
            obj = Prices.objects.filter(~Q(usage_limit=0) & Q(expire_limit=0))
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
            obj = Prices.objects.filter(Q(usage_limit=0) & Q(expire_limit=time))
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
        obj = Prices.objects.get(usage_limit=usage, expire_limit=time, user_limit=iplimit).price
        return Response({'price': f'{obj:,}'})


