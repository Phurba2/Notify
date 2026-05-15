import random
import firebase_admin
from firebase_admin import credentials, messaging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))

def send_html_email(user_email, context, user_type="normal"):
    try:
        if user_type == "professional":
            template_name = "emails/professional_welcome_email.html"
            subject = f"Welcome to {context.get('site_name', 'Our Website')} Professional Network"
        else:
            template_name = "emails/welcome_email.html"
            subject = f"Welcome to {context.get('site_name', 'Our Website')}"

        html_content = render_to_string(template_name, context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=f"Welcome {context.get('name', 'Valued Member')}!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        print("✅ HTML email sent successfully")
        return True

    except Exception as e:
        print("📧 HTML Email Error:", e)
        return False

def send_professional_verification_email(user_email, context):
    try:
        html_content = render_to_string("emails/professional_verification.html", context)

        email = EmailMultiAlternatives(
            subject=f"Verify Your Professional Account - {context.get('site_name')}",
            body=f"Your verification code is {context.get('otp_code')}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        print("✅ Professional verification email sent successfully")
        return True

    except Exception as e:
        print("📧 Professional Verification Email Error:", e)
        return False

def send_forgot_password_email(user_email, context):
    try:
        html_content = render_to_string("emails/forgot_password.html", context)

        email = EmailMultiAlternatives(
            subject=f"Reset Your Password - {context.get('site_name')}",
            body=f"Your password reset OTP is {context.get('otp_code')}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        print("✅ Forgot password email sent successfully")
        return True

    except Exception as e:
        print("📧 Forgot Password Email Error:", e)
        return False

def send_booking_verification_email(user_email, context):
    try:
        html_content = render_to_string("emails/booking_verification.html", context)

        email = EmailMultiAlternatives(
            subject=f"Verify Your Booking - {context.get('site_name')}",
            body=f"Your booking verification code is {context.get('otp_code')}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        print("✅ Booking verification email sent successfully")
        return True

    except Exception as e:
        print("📧 Booking Verification Email Error:", e)
        return False


def init_firebase():
    if firebase_admin._apps:
        return True

    firebase_file = getattr(settings, "FIREBASE_SERVICE_ACCOUNT", None)

    if not firebase_file or not os.path.exists(firebase_file):
        print("⚠️ Firebase service account file not found. Push notification disabled.")
        return False

    cred = credentials.Certificate(firebase_file)
    firebase_admin.initialize_app(cred)
    return True


def send_fcm_push(token, title, body, data=None):
    if not init_firebase():
        raise Exception("Firebase is not configured correctly.")

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        token=token,
    )

    return messaging.send(message)