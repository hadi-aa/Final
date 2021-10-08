from django.contrib import admin
from . import models

admin.site.site_header = 'Costumer Relationship Manager'


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'employees_count',
        # many to many field admin display method
        models.Organization.organization_products_admin,
        'repr_name',
        'repr_num',
        'repr_email',
        'logo',
    )

    list_display_links = (
        'name',
    )

    list_editable = (
        'repr_name',
        'repr_num',
        'repr_email',
        'logo',
    )

    search_fields = (
        'name__icontains',
    )

    list_filter = (
        'name',
        'user',
        'repr_name',
    )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_registered',
        'user',
    )

    list_display_links = (
        'name',
    )

    search_fields = (
        'name__icontains',
    )

    list_filter = (
        'name',
        'user',
    )


@admin.register(models.StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_registered',
        'price',
        'quantity',
        # many to many field admin display method
        models.StockProduct.downstream_product_admin,
        'user',
    )

    list_display_links = (
        'name',
    )

    list_editable = (
        'price',
        'quantity',
    )

    search_fields = (
        'name__icontains',
    )

    list_filter = (
        'name',
        'user',
    )
