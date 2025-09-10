from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alerts/', views.alerts, name='alerts'),
    path('fisheries/', views.fisheries, name='fisheries'),
    path('pollution/', views.pollution, name='pollution'),
    path('safeplaces/', views.safeplaces, name='safeplaces'),
    path('adminfrontend/', views.adminfrontend, name='adminfrontend'),
    
    # API endpoints for SMS functionality and alert creation
    path('api/subscribe-sms/', views.subscribe_sms, name='subscribe_sms'),
    path('api/unsubscribe-sms/', views.unsubscribe_sms, name='unsubscribe_sms'),
    path('api/subscribers/', views.get_subscribers, name='get_subscribers'),
    path('api/alerts/', views.get_active_alerts, name='get_active_alerts'),
    path('api/create-alert/', views.create_alert, name='create_alert'),
    path('api/test-sms/', views.test_sms_service, name='test_sms_service'),
]