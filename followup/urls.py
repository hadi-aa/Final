from django.urls import path
from . import views as followup_views

app_name = 'followup'
urlpatterns = [
    path('organization/quote/list/<int:pk>/', followup_views.OrganizationQuoteList.as_view(), name='organizatonquotelist'),
    path('quote/list/', followup_views.QuoteList.as_view(), name='quote_list'),
    path('quote/<int:pk>/', followup_views.QuoteDetail.as_view(), name='quote'),
    path('quote/create/<int:pk>/', followup_views.create_quote, name='create_quote'),
    path('quote/<int:pk>/pdf/', followup_views.QuotePDF.as_view(), name='quote_pdf'),
    path('quote/email/<int:pk>/', followup_views.send_quote_email, name='quote_email'),
    path('followupreport/create/<int:pk>', followup_views.CreateFollowupReport.as_view(), name='new_followup'),
    path('followupreport/list/', followup_views.FollowupReportList.as_view(), name='followup_list'),
    path('followupreport/<int:pk>/', followup_views.FollowupReport.as_view(), name='followupreport'),
    path('email/list/', followup_views.EmailTaslResultList.as_view(), name='email_list'),
]
