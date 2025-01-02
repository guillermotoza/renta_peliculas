from django.urls import path
from .views import membership_list, membership_detail, subscribe, create_checkout_session, payment_success, payment_cancel
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', membership_list, name='membership_list'),
    path('<slug:membership_slug>/', membership_detail, name='membership_detail'),
    path('<slug:membership_slug>/subscribe/', subscribe, name='subscribe'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('success/', payment_success, name='payment_success'),
    path('cancel/', payment_cancel, name='payment_cancel'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)