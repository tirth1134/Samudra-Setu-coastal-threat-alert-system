import json
from django.conf import settings
from django.utils import timezone
from .models import SMSSubscriber, NotificationLog

try:
    from twilio.rest import Client
except ImportError:
    Client = None
    print("❌ Twilio not installed. Run: pip install twilio")


def send_alert_notifications(alert):
    """
    Send SMS notifications to all active subscribers.
    Returns the count of successfully notified subscribers.
    """
    active_subscribers = SMSSubscriber.objects.filter(is_active=True)
    notified_count = 0

    for subscriber in active_subscribers:
        try:
            notification = NotificationLog.objects.create(
                subscriber=subscriber,
                alert=alert,
                status='pending'
            )

            success = send_sms_via_twilio(subscriber.phone_number, alert)

            if success:
                notification.status = 'sent'
                subscriber.last_notification_sent = timezone.now()
                subscriber.save()
                notified_count += 1
            else:
                notification.status = 'failed'

            notification.save()

        except Exception as e:
            print(f"❌ Failed to send notification to {subscriber.phone_number}: {e}")
            continue

    return notified_count


def send_sms_via_twilio(phone_number, alert):
    """
    Send a single SMS via Twilio API.
    Returns True if sent successfully, False otherwise.
    """
    if Client is None:
        print("❌ Twilio client not available.")
        return False

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_PHONE_NUMBER

    if not all([account_sid, auth_token, twilio_number]):
        print("❌ Twilio credentials not configured!")
        return False

    try:
        client = Client(account_sid, auth_token)

        message_body = (
            f"🚨 COASTAL ALERT 🚨\n\n"
            f"{alert.title}\n"
            f"Severity: {alert.severity.upper()}\n\n"
            f"{alert.description}\n\n"
            f"Stay safe! - Coastal Safety Gujarat"
        )

        formatted_phone = phone_number
        if not phone_number.startswith('+'):
            formatted_phone = f"+91{phone_number}"

        print(f"📱 Sending SMS via Twilio to {formatted_phone}...")

        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=formatted_phone
        )

        print(f"✅ SMS sent successfully to {formatted_phone} (SID: {message.sid})")
        return True

    except Exception as e:
        print(f"❌ Failed to send SMS via Twilio: {e}")
        return False


def send_sms_via_webhook(phone_number, alert):
    """
    Fallback/testing method to simulate SMS sending.
    """
    try:
        message = (
            f"ALERT: {alert.title}\n"
            f"Severity: {alert.severity.upper()}\n"
            f"{alert.description}\n\nStay safe!"
        )

        webhook_data = {
            'to': phone_number,
            'message': message,
            'alert_id': alert.id,
            'timestamp': timezone.now().isoformat()
        }

        print(f"⚠️  SMS Webhook Data (simulation):\n{json.dumps(webhook_data, indent=2)}")
        return True

    except Exception as e:
        print(f"❌ Error sending SMS via webhook: {e}")
        return False