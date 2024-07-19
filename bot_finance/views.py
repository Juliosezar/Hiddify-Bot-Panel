from os import environ
from django.shortcuts import render, redirect
from .models import Prices, ConfirmPaymentQueue, ConfirmTamdidPaymentQueue, BotConfigInfo, OffCodes
from .actions import FinanceAction
from django.views import View
from .forms import DenyForm,AddPriceForm,AddOffForm,EditPriceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from bot_customers.models import Customer
from django.contrib import messages
from bot_config.actions import BotAction
from utils import now_timestamp




class ConfirmPaymentPage(LoginRequiredMixin, View):
    def get(self, request, show_box):
        pay_queue_obj = ConfirmPaymentQueue.objects.filter(status=1)
        pay_tamdid_obj = ConfirmTamdidPaymentQueue.objects.filter(status=1)
        second_pay_queue_obj = ConfirmPaymentQueue.objects.filter(status=2)
        second_tamdid_pay_queue_obj = ConfirmTamdidPaymentQueue.objects.filter(status=2)
        not_paid_obj = BotConfigInfo.objects.filter(paid=False)
        if not not_paid_obj.exists() and not pay_queue_obj.exists() and not second_pay_queue_obj.exists():
            messages.info(request, "پرداختی برای تایید نمانده است. \n برای اطمینان یکبار صفحه را رفرش کنید.")
        return render(request, 'confirm_payment.html',
                      {'confirm': pay_queue_obj, "confirm_count": pay_queue_obj.count() + pay_tamdid_obj.count(),
                       "second_confirm": second_pay_queue_obj, "second_confirm_count": second_pay_queue_obj.count() + second_tamdid_pay_queue_obj.count(),
                       "second_tamdid_pay": second_tamdid_pay_queue_obj,
                       "not_paid": not_paid_obj, "not_paid_count": not_paid_obj.count(),
                       "confirm_tamdid_pay": pay_tamdid_obj,"show_box": show_box})


class FirstConfirmPayment(LoginRequiredMixin, View):
    def get(self, request, obj_id):
        from bot_connection.command_runer import CommandRunner
        model_obj = ConfirmPaymentQueue.objects.get(id=obj_id)
        if model_obj.status == 1:
            FinanceAction.add_to_wallet(model_obj.custumer.chat_id, model_obj.pay_price)
            if model_obj.config_in_queue:
                if Customer.objects.get(chat_id=model_obj.custumer.chat_id).wallet >= model_obj.config_price:
                    CommandRunner.send_msg_to_user(model_obj.custumer.chat_id, "پرداخت شما تایید شد. ✅")
                    BotAction.create_config_from_queue(config_uuid=model_obj.config_uuid)
                else:
                    CommandRunner.send_msg_to_user(model_obj.custumer.chat_id,
                                                   f'کابر گرامی مبلغ {model_obj.pay_price} تومان به کیف پول شما اضافه گردید. این مبلغ برای خرید کانفیک مورد نظر کافی نیست. ')
            else:
                msg = 'پرداخت شما تایید و به کیف پول شما اضافه شد.'
                CommandRunner.send_msg_to_user(model_obj.custumer.chat_id, msg)
            model_obj.status = 2
            model_obj.timestamp = now_timestamp()
            model_obj.save()
            messages.success(request, 'پرداخت با موفقیت تایید و به کاربر ارسال شد.')
        else:
            messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
        return redirect('bot_finance:confirm_payments', 1)


class SecondConfirmPayment(LoginRequiredMixin, View):
    def get(self, request, obj_id):
        from bot_connection.command_runer import CommandRunner
        model_obj = ConfirmPaymentQueue.objects.get(id=obj_id)
        if model_obj.status == 1:
            FinanceAction.add_to_wallet(model_obj.custumer.chat_id, model_obj.pay_price)
            if model_obj.config_in_queue:
                if Customer.objects.get(chat_id=model_obj.custumer.chat_id).wallet >= model_obj.config_price:
                    CommandRunner.send_msg_to_user(model_obj.custumer.chat_id, "پرداخت شما تایید شد. ✅")
                    BotAction.create_config_from_queue(config_uuid=model_obj.config_uuid)
                else:
                    CommandRunner.send_msg_to_user(model_obj.custumer.chat_id,
                                                   f'کابر گرامی مبلغ {model_obj.pay_price} تومان به کیف پول شما اضافه گردید. این مبلغ برای خرید کانفیک مورد نظر کافی نیست. ')
            else:
                msg = 'پرداخت شما تایید و به کیف پول شما اضافه شد.'
                CommandRunner.send_msg_to_user(model_obj.custumer.chat_id, msg)
            model_obj.status = 3
            model_obj.timestamp = now_timestamp()
            model_obj.save()
            messages.success(request, 'پرداخت با موفقیت تایید و به کاربر ارسال شد.')

        elif model_obj.status == 2:
            model_obj.status = 3
            model_obj.timestamp = now_timestamp()
            model_obj.save()
            messages.success(request, 'پرداخت با موفقیت تایید شد.')
            return redirect('bot_finance:confirm_payments', 2)
        # ToDO
        else:
            messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
        return redirect('bot_finance:confirm_payments', 2)


class FirstTamdidConfirmPayment(LoginRequiredMixin, View):
    def get(self, request, obj_id):
        from bot_connection.command_runer import CommandRunner
        model_obj = ConfirmTamdidPaymentQueue.objects.get(id=obj_id)
        if model_obj.status == 1:
            FinanceAction.add_to_wallet(model_obj.config.customer.chat_id, model_obj.pay_price)

            if Customer.objects.get(chat_id=model_obj.config.customer.chat_id).wallet >= model_obj.config_price:
                CommandRunner.send_msg_to_user(model_obj.config.customer.chat_id, "پرداخت شما تایید شد. ✅")
                BotAction.tamdid_config_from_queue(config_uuid=model_obj.config.config_uuid)
            else:
                CommandRunner.send_msg_to_user(model_obj.config.customer.chat_id,
                                               f'کابر گرامی مبلغ {model_obj.pay_price} تومان به کیف پول شما اضافه گردید. این مبلغ برای تمدید سرویس مورد نظر کافی نیست. ')
            model_obj.status = 2
            model_obj.timestamp = now_timestamp()
            model_obj.save()
            messages.success(request, 'پرداخت با موفقیت تایید و به کاربر ارسال شد.')
        else:
            messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
        return redirect('bot_finance:confirm_payments', 1)

class SecondTamdidConfirmPayment(LoginRequiredMixin, View):
    def get(self, request, obj_id):
        from bot_connection.command_runer import CommandRunner
        model_obj = ConfirmTamdidPaymentQueue.objects.get(id=obj_id)
        if model_obj.status == 1:
            FinanceAction.add_to_wallet(model_obj.config.customer.chat_id, model_obj.pay_price)

            if Customer.objects.get(chat_id=model_obj.config.customer.chat_id).wallet >= model_obj.config_price:
                BotAction.tamdid_config_from_queue(config_uuid=model_obj.config.config_uuid)
            else:
                CommandRunner.send_msg_to_user(model_obj.config.customer.chat_id,
                                               f'کابر گرامی مبلغ {model_obj.pay_price} تومان به کیف پول شما اضافه گردید. این مبلغ برای تمدید سرویس مورد نظر کافی نیست. ')

            model_obj.status = 3
            model_obj.timestamp = now_timestamp()
            model_obj.save()
            messages.success(request, 'پرداخت با موفقیت تایید و به کاربر ارسال شد.')

        elif model_obj.status == 2:
            model_obj.status = 3
            model_obj.timestamp = now_timestamp()
            model_obj.save()
            messages.success(request, 'پرداخت با موفقیت تایید شد.')
            return redirect('bot_finance:confirm_payments', 1)
        # ToDO
        else:
            messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
        return redirect('bot_finance:confirm_payments', 1)



class DenyPaymentPage(LoginRequiredMixin, View):
    def get(self, request, obj_id, typ):
        if typ == "buy":
            model_obj = ConfirmPaymentQueue.objects.get(id=obj_id)
        else:
            model_obj = ConfirmTamdidPaymentQueue.objects.get(id=obj_id)
        if model_obj.status != 1:
            messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
            return redirect('bot_finance:confirm_payments', 1)
        form = DenyForm()
        return render(request, 'deny_payment.html', {'obj': model_obj, 'form': form})

    def post(self, request, obj_id, typ):
        from bot_connection.command_runer import CommandRunner
        if typ == "buy":
            model_obj = ConfirmPaymentQueue.objects.get(id=obj_id)
            chat_id = model_obj.custumer.chat_id
        else:
            model_obj = ConfirmTamdidPaymentQueue.objects.get(id=obj_id)
            chat_id = model_obj.config.customer.chat_id
        form = DenyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if model_obj.status == 1:
                msg = "🔴 درخواست پرداخت شما رد شد." '\n' "✍🏻 علت : " f'{cd['reason']}' '\n\n'
                if cd['delete_all_configs']:
                    msg = msg + "🚫 به دلیل تخلف کانفیگ های شما حذف شده است."
                else:
                    if cd['disable_all_configs']:
                        msg = msg + '\n' "🚫 به دلیل تخلف کانفیگ های شما غیرفعال شده است."
                    # TODO
                # TODO

                if cd['ban_user']:
                    msg = msg + '\n' "🚫 به دلیل تخلف شما بن شده و از استفاده از بات محروم میشوید."
                    customer_obj = Customer.objects.get(chat_id=chat_id)
                    customer_obj.active = False
                    customer_obj.save()
                CommandRunner.send_msg_to_user(chat_id, msg)
                model_obj.status = 10
                model_obj.timestamp = now_timestamp()
                model_obj.save()
                messages.success(request, "پرداخت با موفقیت رد تایید شد.")
                return redirect('bot_finance:confirm_payments', 1)

            else:
                messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
                return redirect('bot_finance:confirm_payments', 1)
        return render(request, 'deny_payment.html', {'obj': model_obj, 'form': form})


class DenyPaymentAfterFirsConfirmPage(LoginRequiredMixin, View):
    def get(self, request, obj_id):
        model_obj = ConfirmPaymentQueue.objects.get(id=obj_id)
        if model_obj.status != 2:
            messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
            return redirect('bot_finance:confirm_payments', 2)
        form = DenyForm()
        return render(request, 'deny_payment.html', {'obj': model_obj, 'form': form})

    def post(self, request, obj_id):
        from bot_connection.command_runer import CommandRunner
        model_obj = ConfirmPaymentQueue.objects.get(id=obj_id)
        form = DenyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if model_obj.status == 2:
                msg = "🔴 درخواست پرداخت شما رد شد." '\n' "✍🏻 علت : " f'{cd['reason']}' '\n\n'

                if cd['delete_all_configs']:
                    msg = msg + "🚫 به دلیل تخلف کانفیگ های شما حذف شده است."
                else:
                    if cd['disable_all_configs']:
                        msg = msg + '\n' "🚫 به دلیل تخلف کانفیگ های شما غیرفعال شده است."
                if cd['ban_user']:
                    msg = msg + '\n' "🚫 به دلیل تخلف شما بن شده و از استفاده از بات محروم میشوید."
                    customer_obj = Customer.objects.get(chat_id=model_obj.custumer.chat_id)
                    customer_obj.active = False
                    customer_obj.save()
                CommandRunner.send_msg_to_user(model_obj.custumer.chat_id, msg)
                model_obj.status = 10
                model_obj.timestamp = now_timestamp()
                model_obj.save()
                messages.success(request, "پرداخت با موفقیت رد تایید شد.")
                return redirect('bot_finance:confirm_payments', 2)

            else:
                messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
                return redirect('bot_finance:confirm_payments', 2)
        return render(request, 'deny_payment.html', {'obj': model_obj, 'form': form})


class DenyTamdidPaymentAfterFirsConfirmPage(LoginRequiredMixin, View):
    def get(self, request, obj_id):
        model_obj = ConfirmTamdidPaymentQueue.objects.get(id=obj_id)
        if model_obj.status != 2:
            messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
            return redirect('bot_finance:confirm_payments', 2)
        form = DenyForm()
        return render(request, 'deny_payment.html', {'obj': model_obj, 'form': form})

    def post(self, request, obj_id):
        from bot_connection.command_runer import CommandRunner
        model_obj = ConfirmTamdidPaymentQueue.objects.get(id=obj_id)
        form = DenyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if model_obj.status == 2:
                msg = "🔴 درخواست پرداخت شما رد شد." '\n' "✍🏻 علت : " f'{cd['reason']}' '\n\n'

                if cd['delete_all_configs']:
                    msg = msg + "🚫 به دلیل تخلف کانفیگ های شما حذف شده است."
                else:
                    if cd['disable_all_configs']:
                        msg = msg + '\n' "🚫 به دلیل تخلف کانفیگ های شما غیرفعال شده است."
                if cd['ban_user']:
                    msg = msg + '\n' "🚫 به دلیل تخلف شما بن شده و از استفاده از بات محروم میشوید."
                    customer_obj = Customer.objects.get(chat_id=model_obj.config.customer.chat_id)
                    customer_obj.active = False
                    customer_obj.save()
                CommandRunner.send_msg_to_user(model_obj.config.customer.chat_id, msg)
                model_obj.status = 10
                model_obj.timestamp = now_timestamp()
                model_obj.save()
                messages.success(request, "پرداخت با موفقیت رد تایید شد.")
                return redirect('bot_finance:confirm_payments', 2)
            else:
                messages.error(request, "این پرداخت توسط ادمین دیگری تایید یا رد شده است.")
                return redirect('bot_finance:confirm_payments', 2)


class EditPricePayment(LoginRequiredMixin, View):
    def get(self, request, obj_id, typ):
        form = EditPriceForm
        if typ == "buy":
            model_obj = ConfirmPaymentQueue.objects.get(id=obj_id)
        else:
            model_obj = ConfirmTamdidPaymentQueue.objects.get(id=obj_id)
        return render(request, 'edit_price_payment.html', {'obj': model_obj, 'form': form})

    def post(self, request, obj_id, typ):
        form = EditPriceForm(request.POST)
        if typ == "buy":
            model_obj = ConfirmPaymentQueue.objects.get(id=obj_id)
        else:
            model_obj = ConfirmTamdidPaymentQueue.objects.get(id=obj_id)
        if form.is_valid():
            price = form.cleaned_data['price']
            model_obj.pay_price = price
            model_obj.save()
            messages.success(request, "مبلغ با موفقیت تغییر کرد. از لیست زیر آن را تایید کنید.")
            return redirect('bot_finance:confirm_payments', 1)
        return render(request, 'edit_price_payment.html', {'obj': model_obj, 'form': form})


class PayedAfterCreate(LoginRequiredMixin, View):
    def get(self, request, obj_id):
        try:
            model_obj = BotConfigInfo.objects.get(id=obj_id)
            model_obj.paid = True
            model_obj.save()
            messages.success(request, "پرداخت تایید شد.")
            # TODO: if config disabled ,enable it
        except:
            messages.error(request, "ارور در تایید پرداخت.")
        return redirect("bot_finance:confirm_payments", 3)


class ShowPrices(LoginRequiredMixin, View):
    def get(self, request):
        price_model = Prices.objects.all().order_by('expire_limit', 'usage_limit')
        return render(request, 'show_prices.html', {'price_model': price_model})


class DeleteOrEditPrice(LoginRequiredMixin, View):
    def get(self, request, obj_id, action):
        model_obj = Prices.objects.get(id=obj_id)
        if action == "delete":
            model_obj.delete()
            messages.success(request, "تعرفه با موفقیت حذف شد.")
            return redirect('bot_finance:show_prices')


class AddPrice(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPriceForm()
        return render(request, 'AddPrice.html', {'form': form})

    def post(self, request):
        form = AddPriceForm(request.POST)
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

            Prices.objects.create(
                price=price,
                expire_limit=int(month),
                user_limit=int(ip_limit),
                usage_limit=int(usage),
            ).save()
            return redirect('bot_finance:show_prices')
        return render(request, 'AddPrice.html', {'form': form})


class AddOffCode(LoginRequiredMixin, View):
    def get(self, request):
        form = AddOffForm
        return render(request, "add_off_code.html", {"form": form})

    def post(self, request):
        form = AddOffForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            OffCodes.objects.create(
                type_off=bool(int(cd["type_off"])),
                amount=cd["amount"],
                customer_count=cd["curumer_count"],
                use_count=cd["use_count"],
                create_timestamp=now_timestamp(),
                end_timestamp=now_timestamp() + (int(cd["end_time"]) * 86400),
                for_infinit_usages=cd["for_infinit_usages"],
                for_infinit_times=cd["for_infinit_times"],
                for_not_infinity=cd["for_not_infinity"],
            )
            return redirect("bot_finance:show_off_codes")
        return render(request, "add_off_code.html", {"form": form})


class ShowOffCodes(LoginRequiredMixin, View):
    def get(self, request):
        model_obj = OffCodes.objects.all().order_by('-id')
        BOT_USERNAME = environ.get('BOT_USERNAME')
        return render(request, "show_off_codes.html", {"model_obj":model_obj, "bot_username":BOT_USERNAME})


class DeleteOffCode(LoginRequiredMixin, View):
    def get(self, request, uuid):
        OffCodes.objects.get(uid=uuid).delete()
        return redirect("bot_finance:show_off_codes")

