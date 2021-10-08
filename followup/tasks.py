from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger

from final.celery import app
from followup.email import quote_email


@shared_task
def multiply(x, y):
    return x * y


logger = get_task_logger(__name__)


@app.task
def send_quote_email_task(pk, quote_id, quote_organization, sender):
    logger.info("email send successfully")
    return quote_email(pk)
