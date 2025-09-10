from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from .models import SMSSubscriber, Alert, NotificationLog
from .utils import send_alert_notifications, send_sms_via_twilio

# ======================
# Frontend Views
# ======================

def index(request):
    """
    Main page with latest 10 active alerts.
    """
    alerts = Alert.objects.filter(is_active=True).order_by('-created_at')[:10]
    alert_data = [
        {
            'id': alert.id,
            'title': alert.title,
            'description': alert.description,
            'severity': alert.severity,
            'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'time_ago': get_time_ago(alert.created_at)
        }
        for alert in alerts
    ]

    latest_alert = alerts[0] if alerts else None

    return render(request, 'index.html', {
        'alerts': alert_data,
        'latest_alert': latest_alert
    })

def alerts(request): return render(request, 'alerts.html')
def fisheries(request): return render(request, 'fisheries.html')
def pollution(request): return render(request, 'pollution.html')
def safeplaces(request): return render(request, 'safeplaces.html')

def adminfrontend(request):
    """
    Admin page - only for staff users.
    """
    if not request.user.is_staff:
        return render(request, 'adminfrontend.html', {'error': 'You must be an admin to access this page'})
    return render(request, 'adminfrontend.html')

# ======================
# SMS Subscription Views
# ======================

@csrf_exempt
@require_POST
def subscribe_sms(request):
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number', '').strip()

        if not phone_number:
            return JsonResponse({'success': False, 'error': 'Phone number is required'})
        if len(phone_number) < 10:
            return JsonResponse({'success': False, 'error': 'Invalid phone number'})

        subscriber, created = SMSSubscriber.objects.get_or_create(
            phone_number=phone_number,
            defaults={'is_active': True}
        )

        if not created and subscriber.is_active:
            message = 'Already subscribed to SMS alerts'
        elif not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()
            message = 'Re-activated SMS alerts subscription'
        else:
            message = 'Successfully subscribed to SMS alerts'

        return JsonResponse({'success': True, 'message': message, 'phone_number': phone_number})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def unsubscribe_sms(request):
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number', '').strip()

        if not phone_number:
            return JsonResponse({'success': False, 'error': 'Phone number is required'})

        try:
            subscriber = SMSSubscriber.objects.get(phone_number=phone_number)
            subscriber.is_active = False
            subscriber.save()
            return JsonResponse({'success': True, 'message': 'Successfully unsubscribed from SMS alerts'})
        except SMSSubscriber.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Phone number not found'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_subscribers(request):
    try:
        subscribers = SMSSubscriber.objects.all().order_by('-subscribed_at')
        subscriber_data = [
            {
                'id': s.id,
                'phone_number': s.phone_number,
                'is_active': s.is_active,
                'subscribed_at': s.subscribed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'last_notification_sent': s.last_notification_sent.strftime('%Y-%m-%d %H:%M:%S') if s.last_notification_sent else None
            }
            for s in subscribers
        ]
        return JsonResponse({'success': True, 'subscribers': subscriber_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# ======================
# Alerts & Notifications
# ======================

@csrf_exempt
@require_POST
def create_alert(request):
    """
    Handle alert creation and send notifications to all active subscribers
    """
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        severity = data.get('severity', 'medium').strip()

        # Validate input
        if not title or not description:
            return JsonResponse({'success': False, 'error': 'Title and description are required'})

        if severity not in ['low', 'medium', 'high', 'critical']:
            return JsonResponse({'success': False, 'error': 'Invalid severity level'})

        # Create alert
        alert = Alert.objects.create(
            title=title,
            description=description,
            severity=severity,
            is_active=True
        )

        # Send notifications to all active subscribers
        send_alert_notifications(alert)

        return JsonResponse({
            'success': True,
            'message': 'Alert created and notifications sent successfully',
            'alert_id': alert.id
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def get_active_alerts(request):
    alerts = Alert.objects.filter(is_active=True).order_by('-created_at')[:10]
    alert_data = [
        {
            'id': a.id,
            'title': a.title,
            'description': a.description,
            'severity': a.severity,
            'created_at': a.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'time_ago': get_time_ago(a.created_at)
        }
        for a in alerts
    ]
    return JsonResponse({'alerts': alert_data})

def get_time_ago(dt):
    now = timezone.now()
    diff = now - dt
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"

# ======================
# Test SMS
# ======================

@csrf_exempt
@require_POST
def test_sms_service(request):
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number', '').strip()

        if not phone_number:
            return JsonResponse({'success': False, 'error': 'Phone number is required'})

        test_alert = Alert.objects.create(
            title="SMS Test",
            description="This is a test message.",
            severity="low",
            is_active=True
        )

        success = send_sms_via_twilio(phone_number, test_alert)

        if success:
            return JsonResponse({'success': True, 'message': f'SMS sent to {phone_number}', 'alert_id': test_alert.id})
        else:
            return JsonResponse({'success': False, 'error': 'SMS failed. Check logs.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})