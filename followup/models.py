from decimal import Decimal
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels
from . import enums

'''this model specifies quote details'''


class Quote(models.Model):
    organization = models.ForeignKey('analyse.Organization', on_delete=models.CASCADE)
    date_registered = models.DateTimeField(default=timezone.now, verbose_name='date Registered')
    date_registered_jalali = jmodels.jDateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                             verbose_name='user responsible for registration')
    status = models.CharField(max_length=100, choices=enums.QuoteStatus.choices, blank=True, null=True)

    class Meta:
        ordering = ['-date_registered']
        verbose_name_plural = 'quotes'

    def __str__(self):
        return f'Quote number {self.id} for {self.organization}'

    # this method calculates the sum of total price of each item
    def get_grand_total(self):
        total = 0
        for quote_item in self.quoteitem_set.all():
            total += quote_item.get_quoteitem_total()
        return format(total, ".2f")

    # this method displays the quote items information in admin page
    @admin.display()
    def quote_items(self):
        quote_item_list = QuoteItem.objects.filter(quote_id=self.id)
        return [
            f'{str(quote_item.id)} {str(quote_item.product)} (Price: {quote_item.product.price} | Quantity: {quote_item.quantity} | Discount: {quote_item.discount} %)\n'
            for quote_item in quote_item_list]


'''this model specifies quote item details'''


class QuoteItem(models.Model):
    quote = models.ForeignKey('followup.Quote', on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey('analyse.StockProduct', on_delete=models.PROTECT, )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    ''' discount must be a decimal number between 0.00 to 100.00. the range is checked by validators '''
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=5,
                                   validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(100)])

    '''this method calculates each item total price after tax and discount'''
    def get_quoteitem_total(self):
        tax = 9
        self.product.price -= self.product.price * (self.discount / 100)
        if self.product.taxable:
            self.product.price += self.product.price * tax / 100
        return self.quantity * self.product.price


'''this model specifies followup details'''


class Followup(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                             verbose_name='user responsible for registration')
    date_registered = models.DateTimeField(default=timezone.now, verbose_name='date Registered')
    date_registered_jalali = jmodels.jDateTimeField(auto_now=True)
    organization = models.ForeignKey('analyse.Organization', on_delete=models.CASCADE)
    report = models.TextField(blank=False, null=False, verbose_name='followup report')

    class Meta:
        ordering = ['-date_registered']
        verbose_name_plural = 'followups'

    def __str__(self):
        return f'follow up report number {self.id}'.title()

