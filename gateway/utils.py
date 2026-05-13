import random

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