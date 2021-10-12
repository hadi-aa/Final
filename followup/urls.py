from django.urls import path
from . import views as followup_views

app_name = 'followup'
urlpatterns = [
    path('organization/<int:pk>/quote/list/', followup_views.OrganizationQuoteList.as_view(), name='organizatonquote_list'),
    path('quote/list/', followup_views.QuoteList.as_view(), name='quote_list'),
    path('quote/<int:pk>/', followup_views.QuoteDetail.as_view(), name='quote'),
    path('quote/create/<int:pk>/', followup_views.create_quote, name='create_quote'),
    path('quote/<int:pk>/pdf/', followup_views.QuotePDF.as_view(), name='quote_pdf'),
    path('quote/<int:pk>/email/', followup_views.send_quote_email, name='quote_email'),
    path('followupreport/create/<int:pk>', followup_views.CreateFollowupReport.as_view(), name='create_followupreport'),
    path('followupreport/list/', followup_views.FollowupReportList.as_view(), name='followupreport_list'),
    path('followupreport/<int:pk>/', followup_views.FollowupReport.as_view(), name='followupreport'),
    path('email/list/', followup_views.EmailTaskResultList.as_view(), name='email_list'),
]
