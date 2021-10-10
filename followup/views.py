import io
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django_celery_results.models import TaskResult
from rest_framework import status
from xhtml2pdf import pisa

from analyse.models import StockProduct, Organization
from followup.tasks import send_quote_email_task
from .forms import QuoteItemForm
from .models import Quote, QuoteItem, Followup

'''return all quote of an specific organization'''


class OrganizationQuoteList(LoginRequiredMixin, ListView):
    model = Quote
    paginate_by = 4
    extra_context = {'flag': 'flag'}

    def get_queryset(self):
        return Quote.objects.filter(organization_id=self.kwargs.get('pk'), user__pk=self.request.user.pk)


class QuoteList(LoginRequiredMixin, ListView):
    model = Quote
    paginate_by = 4

    def get_queryset(self):
        """Return user-specific quotes list"""
        return Quote.objects.filter(user__pk=self.request.user.pk)


class QuoteDetail(LoginRequiredMixin, DetailView):
    model = Quote

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.id:
            return redirect('error')
        return super().get(request, *args, **kwargs)


def create_quote(request, pk):
    organization_products = Organization.objects.get(pk=pk).organization_products.all()

    ''' stock products related to organizations products '''
    stock_products = StockProduct.objects.filter(downstream_product__in=organization_products, quantity__gte=1)
    '''                                                  '''

    ''' this section checks if request sent by AJAX is not empty '''
    if request.method == 'POST' and len(json.loads(request.POST.get('quote'))) > 0:

        ajax_quote = json.loads(request.POST.get('quote'))

        ''' a quote object is created. if information related to items are valid this quotes deemed as quote releted to items'''
        quote = Quote.objects.create(organization_id=pk, status='CREATED', user_id=request.user.pk, )

        for item in ajax_quote:
            quoteitemform = QuoteItemForm(ajax_quote[item])
            product = StockProduct.objects.get(id=item)
            quantity = ajax_quote[item]['quantity']
            discount = ajax_quote[item]['discount']

            ''' criteria against which validity of information of item are evaluated: '''
            '''1- item information are valid based on form processing'''
            '''2- the product in item must be one of stock product related to organization products'''
            '''3- the quantity of items should not exceed the quantity in stock'''
            if quoteitemform.is_valid() and product in stock_products and product.quoteitem_quantity_checker(quantity):
                quoteitem = QuoteItem.objects.create(quote_id=quote.pk, product_id=product.pk, quantity=quantity,
                                                     discount=discount, )
            else:

                '''if item information are invalid none of these item will be saved and previously created quote object wil be destroyed'''
                quote.delete()

                return JsonResponse({'success': False}, status=400)
        # return JsonResponse({'success': True, 'quote_id': quote.pk}, status=200)
        return redirect('followup:quote', pk=int(quote.pk))
    context = {
        'stock_products': set(stock_products),
        'organization': Organization.objects.get(pk=pk),
    }
    return render(request, 'followup/quote_form.html', context)


'''************* Report related views *************'''
'''adds a new Report'''


class CreateFollowupReport(LoginRequiredMixin, CreateView):
    model = Followup
    fields = [
        'report',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = Organization.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        form.instance.organization_id = self.kwargs['pk']
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'invalid data')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('analyse:organization',
                            kwargs={'pk': self.object.organization.pk, 'title': self.object.organization.name})


class FollowupReport(LoginRequiredMixin, DetailView):
    model = Followup

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.id:
            return redirect('error')
        return super().get(request, *args, **kwargs)


class FollowupReportList(LoginRequiredMixin, ListView):
    model = Followup

    def get_queryset(self):
        """Returns user-specific followup reportS"""
        return Followup.objects.filter(user__pk=self.request.user.pk)


class QuotePDF(LoginRequiredMixin, DetailView):
    model = Quote
    template_name = 'followup/email.html'
    context_dict = {}

    def render_to_response(self, context, **kwargs):
        pdf = render_to_pdf(self.template_name, context)
        return HttpResponse(pdf, content_type='application/pdf')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()

    # This part will create the pdf.
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required
def send_quote_email(request, pk):
    quote = Quote.objects.get(pk=pk)
    quote_organization = f'organization = {str(quote.organization)}'
    sender = f'user = {str(request.user)}'
    quote_id = f'quote ID = {pk}'
    send_email_task = send_quote_email_task.delay(pk, quote_id, quote_organization, sender)
    print(send_email_task.id)
    print(send_email_task.status)
    print(send_email_task.backend)
    messages.success(request, 'email sent')
    return redirect('followup:quote', pk=pk)


class EmailTaslResultList(LoginRequiredMixin, ListView):
    model = TaskResult
    template_name = 'followup/email_list.html'
