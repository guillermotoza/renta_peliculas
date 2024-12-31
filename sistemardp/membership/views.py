import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Membership, UserMembership, Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def membership_list(request):
    memberships = Membership.objects.all()
    context = {
        'memberships': memberships
    }
    return render(request, 'membership_list.html', context)

@login_required
def membership_detail(request, membership_slug):
    membership = Membership.objects.get(slug=membership_slug)
    context = {
        'membership': membership
    }
    return render(request, 'membership_detail.html', context)

@login_required
def subscribe(request, membership_slug):
    membership = Membership.objects.get(slug=membership_slug)
    user_membership, created = UserMembership.objects.get_or_create(user=request.user)
    user_membership.membership = membership
    user_membership.save()
    Subscription.objects.create(user_membership=user_membership, end_date='2024-12-31')
    return redirect('membership_list')

@login_required
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Membresía Gold',
                },
                'unit_amount': 2000,  # Precio en centavos
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/membership/success/',
        cancel_url='http://localhost:8000/membership/cancel/',
    )
    return redirect(session.url, code=303)

@csrf_exempt
def payment_success(request):
    return render(request, 'membership/payment_success.html')

@csrf_exempt
def payment_cancel(request):
    return render(request, 'membership/payment_cancel.html')