from django.db import models
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.

#categories choices
CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sports Wear'),
    ('OW', 'Outwear')
)

#label
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    label = models.CharField(choices=LABEL_CHOICES , max_length=5)
    slug=models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={
             'slug':self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={
             'slug':self.slug
        })
        
    def get_remove_from_cart_url(self):
        return reverse("core:remove_from_cart", kwargs={
             'slug':self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price
    
    def get_amount_save(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        else:
            return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
