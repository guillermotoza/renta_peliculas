import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Membership, UserMembership, Subscription
from django.utils import timezone

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
    
    # Verificar si el usuario ya tiene una suscripción activa
    active_subscription = Subscription.objects.filter(
        user_membership=user_membership,
        active=True,
        end_date__gt=timezone.now()
    ).exists()

    if active_subscription:
        # Redirigir al usuario con un mensaje de error
        return render(request, 'error.html', {
            'message': 'Ya tienes una membresía activa. No puedes agregar otra hasta que expire.'
        })

    # Crear o actualizar la suscripción
    user_membership.membership = membership
    user_membership.save()
    Subscription.objects.create(user_membership=user_membership, end_date=timezone.now() + timezone.timedelta(days=30))
    
    return redirect('membership_list')

@login_required
def cancel_subscription(request):
    user_membership = UserMembership.objects.get(user=request.user)
    subscription = Subscription.objects.filter(user_membership=user_membership, active=True).first()

    if subscription:
        subscription.active = False
        subscription.end_date = timezone.now()
        subscription.save()
        message = "Tu suscripción ha sido cancelada exitosamente."
    else:
        message = "No tienes una suscripción activa para cancelar."

    return render(request, 'subscription_cancelled.html', {'message': message})

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
                'unit_amount': 2000,  # Precio en centavos (2000 centavos = $20.00)
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
    return render(request, 'payment_success.html')

@csrf_exempt
def payment_cancel(request):
    return render(request, 'payment_cancel.html')