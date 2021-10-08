from django.db import models


class QuoteStatus(models.TextChoices):
    # different status of quote
    created = 'CREATED', 'quote created'
    finalised = 'FINALISED', 'quote finalised'
