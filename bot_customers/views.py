from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Customer
from django.contrib import messages
from bot_config.models import BotConfigInfo
from .forms import SearchUserForm, SendMessageToCustomerForm, ChangeWalletForm, RegisterConfigToCustumerForm
from django.db.models import Q
from bot_finance.models import ConfirmPaymentQueue
from bot_reports.models import CustomerLog
from bot_connection.models import SendMessage
from .actions import CustomerAction


class CustomerList(LoginRequiredMixin, View):
    def get(self, request):
        customer_model = Customer.objects.all()
        form = SearchUserForm()
        return render(request, 'list_custumers.html', {"customer_model": reversed(customer_model), 'search_user':form})

    def post(self, request):
        form = SearchUserForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['search_user']
            customer_model = Customer.objects.filter(Q(chat_id__icontains=word) | Q(first_name__icontains=word) | Q(username__icontains=word))
            if not customer_model.exists():
                messages.error(request, "یوزری با این مشخصات یافت نشد.")
            return render(request, 'list_custumers.html', {"customer_model": reversed(customer_model),'search_user':form})
        return redirect('accounts:home')


class CustomerDetail(LoginRequiredMixin, View):
    def get(self, request, customer_id):
        customer_obj = Customer.objects.get(chat_id=customer_id)
        config_model = BotConfigInfo.objects.filter(customer=customer_obj)
        pay_model = ConfirmPaymentQueue.objects.filter(custumer=customer_obj, status=3)
        sum_pays = sum(item.pay_price for item in pay_model)
        sum_configs = True if len(config_model) > 0 else False

        history = reversed(CustomerLog.objects.filter(customer=customer_obj))
        return render(request, "Custumer_details.html", {"customer_obj": customer_obj, "sum_pays": sum_pays,
                                "history": history, "configs_model": config_model,"sum_configs": sum_configs})


class SendMsgToAll(LoginRequiredMixin, View):
    def get(self, request):
        form = SendMessageToCustomerForm
        return render(request, 'send_msg_to_custumer.html', {"form": form})

    def post(self, request):
        form = SendMessageToCustomerForm(request.POST)
        customer_model = Customer.objects.all()
        if form.is_valid():
            cd = form.cleaned_data
            for i in customer_model:
                SendMessage.objects.create(customer=i, message=cd['message']).save()
            messages.success(request, "پیام شما در لیست ارسال قرار گرفت.")
            return redirect('accounts:home_bot')
        return render(request, 'send_msg_to_custumer.html', {"form": form})


class SendMsgToUser(LoginRequiredMixin, View):
    def get(self, request, userid):
        form = SendMessageToCustomerForm
        return render(request, 'send_msg_to_custumer.html', {"form": form})

    def post(self, request, userid):
        form = SendMessageToCustomerForm(request.POST)
        customer_model = Customer.objects.get(chat_id=userid)
        if form.is_valid():
            msg = form.cleaned_data['message']
            SendMessage.objects.create(customer=customer_model, message=msg).save()
            messages.success(request, "پیام شما در صف ارسال قرارا گرفت.")
            return redirect('bot_customers:custumer_detail', userid)


class ChangeWalletAmount(LoginRequiredMixin, View):
    def get(self, request, userid):
        form = ChangeWalletForm
        return render(request, "change_wallet.html", {"form": form})

    def post(self, request, userid):
        customer_model = Customer.objects.get(chat_id=userid)
        form = ChangeWalletForm(request.POST)
        if form.is_valid():
            wallet = form.cleaned_data['wallet']
            customer_model.wallet = wallet * 1000
            customer_model.save()
            return redirect('bot_customers:custumer_detail', userid)
        return render(request, 'change_wallet.html', {"form": form})


class UpdateCustumer(LoginRequiredMixin, View):
    def get(self, request, userid):
        from bot_connection.command_runer import CommandRunner
        get = CommandRunner.get_user_info(userid)
        CustomerAction.check_custumer_info(userid, get["first_name"], get["username"])
        messages.success(request, "اطلاعات یوزر آپدیت شد.")
        return redirect(request.META.get('HTTP_REFERER', '/'))


class RegisterConfigToCustumer(LoginRequiredMixin, View):
    def get(self, request, conf_uuid):
        form = RegisterConfigToCustumerForm
        config = BotConfigInfo.objects.get(uuid=conf_uuid)
        return render(request, "register_conf_for_customer.html", {"form": form, "config": config})

    def post(self, request, conf_uuid):
        form = RegisterConfigToCustumerForm(request.POST)
        config = BotConfigInfo.objects.get(uuid=conf_uuid)
        if form.is_valid():
            userid = form.cleaned_data['user_id']
            print(userid)
            config.customer = Customer.objects.get(chat_id=userid)
            config.save()
            return redirect("bot_configs:config_page", conf_uuid)
        return render(request, 'register_conf_for_customer.html', {"form": form, "config":config})


class BanUser(LoginRequiredMixin, View):
    def get(self, request, userid):
        from bot_connection.command_runer import CommandRunner
        customer_model = Customer.objects.get(chat_id=userid)
        if customer_model.banned:
            customer_model.banned = False
            CommandRunner.send_msg_to_user(userid, "✅ دسترسی شما به بات توسط ادمین مجاز شد.")
        else:
            customer_model.banned = True
            CommandRunner.send_msg_to_user(userid, "⛔️ دسترسی شما به بات توسط ادمین لغو شد.")
        customer_model.save()
        return redirect("bot_customers:custumer_detail", userid)