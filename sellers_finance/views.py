from django.db.models import Sum
from django.shortcuts import render, redirect
from utils import now_timestamp
from accounts.models import User
from .models import SellersPrices, Payment, SubSellrsRelation
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SellersAddPriceForm, PayForm

class SellersShowPrices(LoginRequiredMixin, View):
    def get(self, request, seller_id):
        price_model = SellersPrices.objects.filter(seller_id=seller_id).order_by('expire_limit', 'usage_limit')
        seller = User.objects.get(id=seller_id)
        return render(request, 'sellers_show_prices.html', {'price_model': price_model, "seller": seller})


class SellersDeleteOrEditPrice(LoginRequiredMixin, View):
    def get(self, request, obj_id):
        model_obj = SellersPrices.objects.get(id=obj_id)
        model_obj.delete()
        messages.success(request, "تعرفه با موفقیت حذف شد.")
        return redirect(request.META.get('HTTP_REFERER', '/'))


class SellersAddPrice(LoginRequiredMixin, View):
    def get(self, request, seller_id):
        form = SellersAddPriceForm(seller_id=seller_id)
        return render(request, 'SelleraAddPrice.html', {'form': form})

    def post(self, request, seller_id):
        form = SellersAddPriceForm(request.POST, seller_id=seller_id)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["type_conf"] == "limited":
                usage = cd["usage"]
                month = cd["month"]
                ip_limit = 0
            elif cd["type_conf"] == "inf_usage":
                usage = 0
                month = cd['month']
                ip_limit = cd["ip_limit"]
            elif cd["type_conf"] == "inf_time":
                usage = cd["usage"]
                month = 0
                ip_limit = 0
            price = cd["price"] * 1000

            SellersPrices.objects.create(
                seller=User.objects.get(id=seller_id),
                price=price,
                expire_limit=int(month),
                user_limit=int(ip_limit),
                usage_limit=int(usage),
            ).save()
            return redirect('sellers_finance:sellers_show_prices', seller_id)
        return render(request, 'AddPrice.html', {'form': form})


class PaymentsPage(LoginRequiredMixin, View):
    def get(self, request):
        child_sellers = {user.child_seller: user.parent_seller for user in SubSellrsRelation.objects.all()}
        print(child_sellers)
        users_pays = {user: 0 for user in User.objects.all() if user not in child_sellers.keys()}
        sum_pays = 0
        for pay in Payment.objects.all():
            if pay.seller in child_sellers.keys():
                users_pays[child_sellers[pay.seller]] += pay.amount
            else:
                users_pays[pay.seller] += pay.amount
            sum_pays += pay.amount
        return render(request, "payments_page.html", {"users_pays":users_pays, "sum_pays":sum_pays})


class SellerPaymentsPage(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        sellers = [seller.child_seller for seller in SubSellrsRelation.objects.filter(parent_seller_id=kwargs.get('seller_id'))]
        sellers.append(User.objects.get(id=kwargs.get('seller_id')))
        self.pays_obj = Payment.objects.filter(seller__in=sellers).order_by('-timestamp')
        self.sum_pays = self.pays_obj.aggregate(Sum('amount'))["amount__sum"] or 0
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, seller_id):
        form = PayForm
        return render(request, "seller_payment.html", {"seller_id": seller_id, "form": form, "sum_pays": self.sum_pays, "pays_obj":self.pays_obj})

    def post(self, request, seller_id):
        form = PayForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount == 0 and Payment.objects.filter(seller_id=seller_id).last().amount <= 0:
                Payment.objects.filter(seller_id=seller_id).last().delete()
            else:
                Payment.objects.create(
                    seller=User.objects.get(id=seller_id),
                    amount=amount * -1000,
                    timestamp=now_timestamp(),
                    created_by=request.user,
                    description="پرداخت بدهی"
                )
            return redirect("sellers_finance:seller_payment_page", seller_id)
        return render(request, "seller_payment.html", {"seller_id": seller_id, "form": form, "sum_pays": self.sum_pays, "pays_obj":self.pays_obj})





