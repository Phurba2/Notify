import json
import threading

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import NotificationHistory, ProfessionalOTP
from .utils import (
    send_html_email,
    send_professional_verification_email,
    generate_otp,
)

class NotifyView(APIView):
    def post(self, request):
        if request.headers.get("X-API-KEY") != "furba":
            return Response({"error": "Unauthorized"}, status=401)

        data = request.data

        user_name = data.get("name", "Valued Member")
        user_email = data.get("email")
        user_type = data.get("user_type", "normal")

        if not user_email:
            return Response({"error": "Email is required"}, status=400)

        # 1. Create DB record
        notif = NotificationHistory.objects.create(
            recipient_name=user_name,
            message="Welcome HTML Email",
            notify_type="MAIL",
            status="PENDING",
        )

        # 2. Prepare context for .html
        context = {
            "name": user_name,
            "email": user_email,
            "user_id": notif.id,
            "reg_id": notif.id,
            "site_name": "My Super Website",
            "login_url": "https://yourwebsite.com/login",
            "dashboard_url": "https://elitefreelancers.org/dashboard/",
            "created_at": timezone.now().strftime("%B %d, %Y"),
            "phone": data.get("phone"),
            "expertise": data.get("expertise"),
            "location": data.get("location"),
            "map_url": data.get("map_url"),
        }

        def worker():
            success = send_html_email(user_email, context, user_type=user_type)

            notif.status = "SENT" if success else "FAILED"
            notif.save()

        threading.Thread(target=worker, daemon=True).start()

        return Response({"status": "Email is being sent!"}, status=202)


@csrf_exempt
def webhook_receiver(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("📩 Webhook received:", data)

            return JsonResponse({
                "status": "received",
                "data": data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON"
            }, status=400)

    return JsonResponse({
        "error": "Only POST method allowed"
    }, status=405)

class ProfessionalVerificationView(APIView):
    def post(self, request):
        if request.headers.get("X-API-KEY") != "furba":
            return Response({"error": "Unauthorized"}, status=401)

        data = request.data

        professional_name = data.get("name", "Professional")
        user_email = data.get("email")
        expertise = data.get("expertise", "Not specified")

        if not user_email:
            return Response({"error": "Email is required"}, status=400)

        otp_code = generate_otp()

        notif = NotificationHistory.objects.create(
            recipient_name=professional_name,
            message=f"Professional Verification OTP: {otp_code}",
            notify_type="MAIL",
            status="PENDING",
        )

        context = {
            "site_name": "My Super Website",
            "site_domain": "mysuperwebsite.com",
            "reference_id": notif.id,
            "otp_code": otp_code,
            "expires_in": 10,
            "professional_name": professional_name,
            "email": user_email,
            "expertise": expertise,
            "verification_url": "http://127.0.0.1:8000/professional/verify/",
            "support_phone": "+977-9800000000",
        }

        success = send_professional_verification_email(user_email, context)

        notif.status = "SENT" if success else "FAILED"
        notif.save()

        return Response({
            "status": "Verification email sent" if success else "Verification email failed",
            "reference_id": notif.id,
        }, status=200 if success else 500)

class ProfessionalSignupView(APIView):
    def post(self, request):
        if request.headers.get("X-API-KEY") != "furba":
            return Response({"error": "Unauthorized"}, status=401)

        data = request.data

        name = data.get("name", "Professional")
        email = data.get("email")
        expertise = data.get("expertise", "Not specified")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        otp_code = generate_otp()

        professional_otp = ProfessionalOTP.objects.create(
            name=name,
            email=email,
            expertise=expertise,
            otp_code=otp_code,
        )

        notif = NotificationHistory.objects.create(
            recipient_name=name,
            message="Professional Verification OTP",
            notify_type="MAIL",
            status="PENDING",
        )

        context = {
            "site_name": "My Super Website",
            "site_domain": "mysuperwebsite.com",
            "reference_id": professional_otp.id,
            "otp_code": otp_code,
            "expires_in": 10,
            "professional_name": name,
            "email": email,
            "expertise": expertise,
            "verification_url": "http://127.0.0.1:8000/professional/verify/",
            "support_phone": "+977-9800000000",
        }

        def worker():
            success = send_professional_verification_email(email, context)
            notif.status = "SENT" if success else "FAILED"
            notif.save()

        threading.Thread(target=worker, daemon=True).start()

        return Response({
            "status": "OTP verification email is being sent",
            "reference_id": professional_otp.id,
        }, status=202)


class ProfessionalVerifyOTPView(APIView):
    def post(self, request):
        if request.headers.get("X-API-KEY") != "furba":
            return Response({"error": "Unauthorized"}, status=401)

        reference_id = request.data.get("reference_id")
        otp_code = request.data.get("otp_code")

        if not reference_id or not otp_code:
            return Response({
                "error": "reference_id and otp_code are required"
            }, status=400)

        try:
            professional_otp = ProfessionalOTP.objects.get(id=reference_id)
        except ProfessionalOTP.DoesNotExist:
            return Response({"error": "Invalid reference ID"}, status=404)

        if professional_otp.is_verified:
            return Response({"status": "Already verified"}, status=200)

        if professional_otp.is_expired():
            return Response({"error": "OTP has expired"}, status=400)

        if professional_otp.otp_code != str(otp_code):
            return Response({"error": "Invalid OTP"}, status=400)

        professional_otp.is_verified = True
        professional_otp.save()

        notif = NotificationHistory.objects.create(
            recipient_name=professional_otp.name,
            message="Professional Welcome Email",
            notify_type="MAIL",
            status="PENDING",
        )

        context = {
            "name": professional_otp.name,
            "email": professional_otp.email,
            "reg_id": professional_otp.id,
            "user_id": professional_otp.id,
            "site_name": "My Super Website",
            "dashboard_url": "https://elitefreelancers.org/dashboard/",
            "created_at": timezone.now().strftime("%B %d, %Y"),
            "phone": "",
            "expertise": professional_otp.expertise,
            "location": "",
            "map_url": "",
        }

        def worker():
            success = send_html_email(
                professional_otp.email,
                context,
                user_type="professional"
            )
            notif.status = "SENT" if success else "FAILED"
            notif.save()

        threading.Thread(target=worker, daemon=True).start()

        return Response({
            "status": "Professional verified. Welcome email is being sent."
        }, status=200)