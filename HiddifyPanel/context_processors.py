from accounts.models import User
from sellers_finance.models import SubSellrsRelation
def list_subsellers(request):
    if request.user.is_authenticated:
        if request.user.level_access == 10:
            sellers_list = [seller for seller in User.objects.filter(level_access__in=[0, 1])]
        elif request.user.level_access == 1:
            sellers_list = [seller.child_seller for seller in SubSellrsRelation.objects.filter(parent_seller=request.user)]
        else:
            sellers_list = None
        return {'sellers_list': sellers_list}
    else:
        return {'sellers_list': None}