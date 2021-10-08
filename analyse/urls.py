from django.urls import path
from . import views

app_name = 'analyse'
urlpatterns = [
    path('Organization/create/', views.CreateOrganization.as_view(), name='new_organization'),
    path('Organization/edit/<int:pk>', views.EditOrganization.as_view(), name='edit_organization'),
    path('Organization/<int:pk>/<str:title>', views.OrganizationDetail.as_view(), name='organization'),
    path('Organization/list/', views.OrganizationList.as_view(), name='organization_list'),
    path('Organization/delete/<int:pk>/', views.DeleteOrganization.as_view(), name='delete_organization'),
    path('Product/create/', views.CreateProduct.as_view(), name='new_product'),
    path('Product/edit/<int:pk>', views.EditProduct.as_view(), name='edit_product'),
    path('Product/<int:pk>/', views.ProductDetail.as_view(), name='product'),
    path('Product/list/', views.ProductList.as_view(), name='product_list'),
    path('StockProduct/create/', views.CreateStockProduct.as_view(), name='new_stockproduct'),
    path('StockProduct/<int:pk>/', views.StockProductDetail.as_view(), name='stockproduct'),
    path('StockProduct/edit/<int:pk>', views.EditStockProduct.as_view(), name='edit_stockproduct'),
    path('StockProduct/list/', views.StockProductList.as_view(), name='stockproduct_list'),
]
