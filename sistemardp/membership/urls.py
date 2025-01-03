from django.urls import path
from .views import membership_list, membership_detail, subscribe, create_checkout_session, payment_success, payment_cancel, cancel_subscription
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('memberships/', membership_list, name='membership_list'),
    path('memberships/<slug:membership_slug>/', membership_detail, name='membership_detail'),
    path('subscribe/<slug:membership_slug>/', subscribe, name='subscribe'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('membership/success/', payment_success, name='payment_success'),
    path('membership/cancel/', payment_cancel, name='payment_cancel'),
    path('cancel-subscription/', cancel_subscription, name='cancel_subscription'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)