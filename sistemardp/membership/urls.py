from django.urls import path
from . import views

urlpatterns = [
    path('memberships/', views.membership_list, name='membership_list'),
    path('memberships/<slug:membership_slug>/', views.membership_detail, name='membership_detail'),
    path('subscribe/<slug:membership_slug>/', views.subscribe, name='subscribe'),
    path('complete_subscription/<slug:membership_slug>/<int:user_id>/', views.complete_subscription, name='complete_subscription'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]