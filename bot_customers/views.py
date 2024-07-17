from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Customer
from servers.models import BotConfigInfo

# Create your views here.
class CustomerList(LoginRequiredMixin, View):
    pass
    # def get(self, request):
    #     customer_model = CustomerModel.objects.all()
    #     form = SearchUserForm()
    #     return render(request, 'list_custumers.html', {"customer_model": reversed(customer_model), 'search_user':form})
    #
    # def post(self, request):
    #     form = SearchUserForm(request.POST)
    #     if form.is_valid():
    #         word = form.cleaned_data['search_user']
    #         customer_model = CustomerModel.objects.filter(Q(userid__icontains=word) | Q(first_name__icontains=word) | Q(username__icontains=word))
    #         if not customer_model.exists():
    #             messages.error(request, "یوزری با این مشخصات یافت نشد.")
    #         return render(request, 'list_custumers.html', {"customer_model": reversed(customer_model),'search_user':form})
    #     return redirect('accounts:home')


class CustomerDetail(LoginRequiredMixin, View):
    def get(self, request, customer_id):
        pass
        # customer_obj = Customer.objects.get(userid=customer_id)
        # config_model = BotConfigInfo.objects.filter(chat_id=customer_obj)
        # pay_model = ConfirmPaymentQueue.objects.filter(custumer=customer_obj, status=3)
        # sum_pays = sum(item.pay_price for item in pay_model)
        # sum_configs = True if len(config_model) > 0 else False
        #
        # # history = reversed(CustomerLog.objects.filter(customer=customer_obj))
        # return render(request, "Custumer_details.html", {"customer_obj": customer_obj, "sum_pays": sum_pays,
        #                                                  "history": history, "configs_model": config_model,
        #                                                  "sum_configs": sum_configs})
