import json


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse

from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView, DeleteView

from followup.models import Followup
from .models import Product, Organization, StockProduct

'''home page view'''


class Home(TemplateView):
    template_name = 'home.html'


'''error page view'''


class Error(TemplateView):
    template_name = 'error.html'


'''************* Organization related views *************'''
'''adds a new Organization'''


class CreateOrganization(LoginRequiredMixin, CreateView):
    model = Organization
    fields = (
        'name',
        'country',
        'employees_count',
        'organization_products',
        'repr_name',
        'repr_email',
        'repr_num',
        'logo',
    )

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'invalid data')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('analyse:organization_list')


'''edit an organization'''


class EditOrganization(LoginRequiredMixin, UpdateView):
    model = Organization
    fields = (
        'name',
        'country',
        'employees_count',
        'organization_products',
        'repr_name',
        'repr_num',
        'repr_email',
        'logo',
    )

    def form_valid(self, form):
        # check section check the user
        if form.instance.user_id != self.request.user.pk:
            return redirect('error')
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('analyse:organization', kwargs={'pk': self.object.pk, 'title': self.object.name})

    def form_invalid(self, form):
        messages.error(self.request, 'invalid data')
        return super().form_invalid(form)


'''single organization'''


class OrganizationDetail(LoginRequiredMixin, DetailView):
    model = Organization

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user.id != self.request.user.id:
            return redirect('error')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        '''stock product related to organization product'''
        stock_products = StockProduct.objects.filter(downstream_product__organization=obj)
        '''                                           '''

        ''' organization followup reports '''
        followup_reports = Followup.objects.filter(organization_id=self.kwargs.get('pk'))
        '''                                '''

        context = super().get_context_data(**kwargs)
        context['stock_products'] = set(stock_products)
        context['followup_reports'] = followup_reports
        return context


'''list of organizations'''


class OrganizationList(LoginRequiredMixin, ListView):
    model = Organization
    paginate_by = 4

    def get_queryset(self):
        queryset = Organization.objects.filter(user__pk=self.request.user.pk)
        """Returns user-specific organization"""
        return queryset

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        query_set = Organization.objects.filter(name__iexact=query)
        query_result = {}
        if len(query_set) > 0:
            for query in query_set:
                query_result[str(query.id)] = query.name
                print(query_result)
            # print(query_set)
            # print('////')
            # print(len(query_set))
            return JsonResponse({'success': True, 'result':query_result}, status=200)
        else:
            print('0')
        return super().get(request, *args, **kwargs)


'''Delete an organization'''


class DeleteOrganization(DeleteView):
    model = Organization
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('analyse:organization_list')

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        # only the user who registered organization can delete it
        if obj.user.id != self.request.user.id:
            return redirect('error')
        return super().get(request, *args, **kwargs)


'''************* Product related views *************'''
'''adds a new Product'''


class CreateProduct(LoginRequiredMixin, CreateView):
    model = Product
    fields = (
        'name',
        'description',
    )

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'invalid data')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('analyse:product', kwargs={'pk': self.object.id})


'''edit a Product'''


class EditProduct(LoginRequiredMixin, UpdateView):
    model = Product
    fields = (
        'name',
        'description',
    )

    def form_valid(self, form):
        if form.instance.user_id != self.request.user.pk:
            return redirect('error')
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('analyse:product', kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        messages.error(self.request, 'invalid data')
        return super().form_invalid(form)


'''product detail'''


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        obj = self.get_object()

        ''' stock product related to product '''
        stock_products = StockProduct.objects.filter(downstream_product__id=obj.id)
        '''                                  '''

        context = super().get_context_data(**kwargs)
        context['stock_products'] = stock_products
        return context


'''list of product'''


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'analyse/product_list.html'


'''************* Stock Product related views *************'''
'''adds a Stock Product'''


class CreateStockProduct(LoginRequiredMixin, CreateView):
    model = StockProduct
    fields = (
        'name',
        'description',
        'price',
        'taxable',
        'quantity',
        'catalogue_image',
        # '''This field is specifies all other product which need this product in the process of production'''
        'downstream_product',
    )

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        messages.success(self.request, 'Product has been successfully added')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'invalid data')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('analyse:stockproduct', kwargs={'pk': self.object.id})


'''stock product detail'''


class StockProductDetail(LoginRequiredMixin, DetailView):
    model = StockProduct


'''edit a Stock Product'''


class EditStockProduct(LoginRequiredMixin, UpdateView):
    model = StockProduct
    fields = (
        'name',
        'description',
        'price',
        'taxable',
        'quantity',
        'catalogue_image',
        # '''This field is specifies all other product which need this product in the process of production'''
        'downstream_product',
    )

    def form_valid(self, form):
        if form.instance.user_id != self.request.user.pk:
            return redirect('error')
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('analyse:stockproduct', kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        messages.error(self.request, 'invalid data')
        return super().form_invalid(form)


'''list of Stock Products'''


class StockProductList(LoginRequiredMixin, ListView):
    model = StockProduct
    template_name = 'analyse/stockproduct_list.html'
