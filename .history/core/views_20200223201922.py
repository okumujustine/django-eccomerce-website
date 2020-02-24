from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,ListView, View
from django.utils import timezone
from .models import Item, OrderItem,  Order, BillingAddress, Payment
from .forms import CheckoutForm
import stripe
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutView(View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request, 'checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # same_shipping_address = forms.cleaned_data.get('same_billing_address')
                # save_info = forms.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip =  zip

                )
                billing_address.save()
                order.billing_address = billing_address
                order.save( )
                return redirect('core:checkout')
            messages.warning(self.request, "Failed Checkout")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('core:order-summary')

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "payment-page.html")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        charge = stripe.Charge.create(
            amount=order.get_total() * 100,
            currency='usd',
            source = token
            # description='Charge for jean',
        )

        order.ordered = True
        payment = Payment()

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
            return render(self.request, 'order-summary-page.html', context)
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
            return redirect("core:order-summary") 
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("core:order-summary")


@login_required
def remove_single_item_from_cart(request, slug):
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
            if  order_item.quantity > 1:   
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            return redirect("core:order-summary")
        else:
            #add message saying the order doesnot contain any item
            messages.info(request, "This item was not in your cart")
            return redirect("core:order-summary",slug=slug)
    else:
        #add message saying user doesnot have any item
        messages.info(request, "You do not have an active order")
        return redirect("core:product",slug=slug)
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
            messages.info(request, "This item was not in your cart")
            return redirect("core:product",slug=slug)
    else:
        #add message saying user doesnot have any item
        messages.info(request, "You do not have an active order")
        return redirect("core:product",slug=slug)
    return redirect("core:product",slug=slug)
