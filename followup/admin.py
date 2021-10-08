from django.contrib import admin
from . import models


@admin.register(models.Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'organization',
        'date_registered',
        models.Quote.quote_items,
    )

    list_filter = (
        'organization',
    )


@admin.register(models.QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'quote',
        'product',
        'quantity',
        'discount',
    )

    list_display_links = ['pk']

    list_filter = (
        'quote',
    )
