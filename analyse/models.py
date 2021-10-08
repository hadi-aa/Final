from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from django_jalali.db import models as jmodels

phone_regex = RegexValidator(regex='^09(1[0-9]|3[1-9]|2[1-9]0[1-9])-?[0-9]{3}-?[0-9]{4}', message='invalid entry')

'''This model specifies the detail of all product'''


class Product(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='user responsible for registration', blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name='name of product')
    description = models.TextField(blank=True, verbose_name='Description', help_text="technical description of product")
    date_registered = models.DateTimeField(default=timezone.now, verbose_name='registration date of the Product')
    date_registered_jalali = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name.title()


'''This models specifies the detail of the Organization'''


class Organization(models.Model):
    name = models.CharField(max_length=200, verbose_name='name')
    country = CountryField()
    logo = models.ImageField(null=True, blank=True, default='default.jpg')
    employees_count = models.PositiveIntegerField(default=1, verbose_name='number of employees')
    organization_products = models.ManyToManyField(Product, through='OrganizationProduct', blank=True)
    repr_name = models.CharField(max_length=200, verbose_name='name of representative')
    repr_num = models.CharField(validators=[phone_regex], max_length=11, unique=True,
                                verbose_name='phone number of representative')
    repr_email = models.EmailField(max_length=254, verbose_name='Email of representative')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='user responsible for registration')
    date_registered = models.DateTimeField(default=timezone.now, verbose_name='registration date')
    date_registered_jalali = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'organizations'
        unique_together = [
            'name',
            'user',
        ]

    def __str__(self):
        return self.name.title()

    # method to display many to many field in admin page
    @admin.display()
    def organization_products_admin(self):
        return [organization_product for organization_product in self.organization_products.all()]


'''Organization Product table'''


class OrganizationProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class StockProduct(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='user responsible for registration', blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name='name')
    description = models.TextField(blank=True, verbose_name='Description', help_text="technical description")
    price = models.PositiveIntegerField(null=True, blank=True, default=0)
    taxable = models.BooleanField(default=True, help_text='Is product subjected to taxation?')
    quantity = models.PositiveIntegerField(verbose_name='quantity in stock')
    catalogue_image = models.ImageField(blank=True, verbose_name='catalogue image')
    '''This field is specifies all other product which need this product in the process of production'''
    downstream_product = models.ManyToManyField(Product, blank=True, verbose_name='Downstream Products')
    ''''''
    date_registered = models.DateTimeField(default=timezone.now, verbose_name='registration date')
    date_registered_jalali = jmodels.jDateTimeField(auto_now=True, verbose_name='registration date')

    def __str__(self):
        return self.name.title()

    @admin.display()
    def downstream_product_admin(self):
        return [i.name for i in self.downstream_product.all()]

    def in_stock(self):
        if self.quantity > 0:
            return True

    def quoteitem_quantity_checker(self, quote_quantity):
        try:
            if self.quantity > float(quote_quantity) > 0:
                return True
        except ValueError:
            return False
