from django.core.mail import EmailMessage
from django.conf import settings
import os

from django.template.loader import get_template

from followup.models import Quote

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final.settings")


def quote_email(pk):
    quote = Quote.objects.get(pk=pk)
    context = {'quote': quote}
    email_body = get_template('followup/email.html').render(context)
    email_subject = f'DETAIL OF QUOTE NUMBER {quote.id}'
    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [quote.organization.repr_email, ],
    )
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    print("Mail successfully sent")
