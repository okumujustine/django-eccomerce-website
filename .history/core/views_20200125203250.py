from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,ListView, View
from django.utils import timezone
from .models import Item, OrderItem,  Order
# Create your views here.


def checkout(request):
    return render(request, 'checkout-page.html')

def products(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request, 'product-page.html', context)


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home-page.html'

 
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
            'object':order
            }
            return render(self.request, 'order-summary-page.html')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated in your cart")
            return redirect("core:product",slug=slug) 
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect("core:product",slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("core:product",slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered = False
                )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed to your cart")
            return redirect("core:product",slug=slug)
        else:
            #add message saying the order doesnot contain any item
            messages.info(request, "This item w as not in your cart")
            return redirect("core:product",slug=slug)
    else:
        #add message saying user doesnot have any item
        messages.info(request, "You do not have an active order")
        return redirect("core:product",slug=slug)
    return redirect("core:product",slug=slug)
