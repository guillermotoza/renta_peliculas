import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Membership, UserMembership, Subscription
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

def membership_list(request):
    memberships = Membership.objects.exclude(membership_type='Free')
    return render(request, 'membership_list.html', {'memberships': memberships})

def membership_detail(request, membership_slug):
    membership = Membership.objects.get(slug=membership_slug)
    return render(request, 'membership_detail.html', {'membership': membership})


def subscribe(request, membership_slug):
    membership = get_object_or_404(Membership, slug=membership_slug)
    
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión o crear una cuenta para obtener una membresía.")
        return redirect('membership_detail', membership_slug=membership_slug)
    
    user_membership, created = UserMembership.objects.get_or_create(user=request.user)
    
    # Verificar si el usuario ya tiene una suscripción activa
    active_subscription = Subscription.objects.filter(
        user_membership=user_membership,
        active=True,
        end_date__gt=timezone.now()
    ).first()

    if active_subscription:
        active_membership_type = user_membership.membership.membership_type
        return render(request, 'error.html', {
            'message': f'Ya tienes una membresía activa ({active_membership_type}). No puedes agregar otra hasta que expire.'
        })

    # Crear una sesión de pago
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'mxn',
                'product_data': {'name': membership.membership_type},
                'unit_amount': int(membership.price * 100),  # Convertir a centavos
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'http://localhost:8000/membership/complete_subscription/{membership_slug}/{request.user.id}/',
        cancel_url='http://localhost:8000/membership/cancel/',
    )
    return redirect(session.url, code=303)

@csrf_exempt
def complete_subscription(request, membership_slug, user_id):
    user = User.objects.get(id=user_id)
    membership = Membership.objects.get(slug=membership_slug)
    user_membership = UserMembership.objects.get(user=user)
       
    # Crear o actualizar la suscripción
    user_membership.membership = membership
    user_membership.save()
    Subscription.objects.create(user_membership=user_membership, end_date=timezone.now() + timezone.timedelta(days=30))
    
    # Enviar correo de confirmación
    send_mail(
        'Confirmación de Membresía',
        f'Hola {user.username},\n\n'
        f'¡Gracias por suscribirte a la membresía {membership.membership_type}!\n\n'
        'Estamos encantados de tenerte como miembro de nuestra comunidad. Aquí tienes algunos detalles importantes sobre tu membresía:\n\n'
        f'- Tipo de Membresía: {membership.membership_type}\n'
        f'- Precio: ${membership.price}\n'
        f'- Descripción: {membership.description}\n\n'
        f'Tu membresía estará activa hasta el {user_membership.subscription_set.latest("end_date").end_date.strftime("%d/%m/%Y")}. '
        'Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos.\n\n'
        '¡Disfruta de todos los beneficios que ofrecemos y gracias por elegirnos!\n\n'
        'Saludos cordiales,\n'
        'El equipo de Renta de Películas',
        'juan.torresz@fgr.org.mx',
        [user.email], 
        fail_silently=False,
    )
    
    return redirect('payment_success')

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

@csrf_exempt
def payment_success(request):
    if 'carro' not in request.session:
        request.session['carro'] = {}
    return render(request, 'payment_success.html')

@csrf_exempt
def payment_cancel(request):
    return render(request, 'payment_cancel.html')