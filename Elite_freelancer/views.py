import json
import threading

from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Mail, Inapp, Booking, PushToken

from rest_framework.permissions import IsAuthenticated, AllowAny

from .utils import (
    send_html_email,
    send_professional_verification_email,
    generate_otp,
    send_forgot_password_email,
    send_booking_verification_email,
    send_fcm_push,
)


class NotifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user_name = data.get("name", "Valued Member")
        user_email = data.get("email")
        user_type = data.get("user_type", "normal")

        if not user_email:
            return Response({"error": "Email is required"}, status=400)

        notif = Mail.objects.create(
            user=user_name,
            email=user_email,
            message="Welcome HTML Email",
            status="PENDING",
        )

        context = {
            "name": user_name,
            "email": user_email,
            "user_id": notif.id,
            "reg_id": notif.id,
            "site_name": "Elite Agency",
            "login_url": "https://elitefreelancer.org/login.php",
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
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


class ProfessionalVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        professional_name = data.get("name", "Professional")
        user_email = data.get("email")
        expertise = data.get("expertise", "Not specified")

        if not user_email:
            return Response({"error": "Email is required"}, status=400)

        otp_code = generate_otp()
        reference_id = f"pro_verify_{user_email}"

        cache.set(
            reference_id,
            {
                "name": professional_name,
                "email": user_email,
                "expertise": expertise,
                "otp_code": otp_code,
            },
            timeout=600,
        )

        notif = Mail.objects.create(
            user=professional_name,
            email=user_email,
            message="Professional Verification OTP",
            status="PENDING",
        )

        context = {
            "site_name": "Elite Agency",
            "site_domain": "elitefreelancer.org",
            "reference_id": reference_id,
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
            "reference_id": reference_id,
        }, status=200 if success else 500)


class ProfessionalSignupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        name = data.get("name", "Professional")
        email = data.get("email")
        expertise = data.get("expertise", "Not specified")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        otp_code = generate_otp()
        reference_id = f"pro_signup_{email}"

        cache.set(
            reference_id,
            {
                "name": name,
                "email": email,
                "expertise": expertise,
                "otp_code": otp_code,
            },
            timeout=600,
        )

        notif = Mail.objects.create(
            user=name,
            email=email,
            message="Professional Verification OTP",
            status="PENDING",
        )

        context = {
            "site_name": "Elite Agency",
            "site_domain": "elitefreelancer.org",
            "reference_id": reference_id,
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
            "reference_id": reference_id,
        }, status=202)


class ProfessionalVerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reference_id = request.data.get("reference_id")
        otp_code = request.data.get("otp_code")

        if not reference_id or not otp_code:
            return Response({
                "error": "reference_id and otp_code are required"
            }, status=400)

        otp_data = cache.get(reference_id)

        if not otp_data:
            return Response({"error": "OTP expired or invalid"}, status=400)

        if otp_data["otp_code"] != str(otp_code):
            return Response({"error": "Invalid OTP"}, status=400)

        cache.delete(reference_id)

        notif = Mail.objects.create(
            user=otp_data["name"],
            email=otp_data["email"],
            message="Professional Welcome Email",
            status="PENDING",
        )

        context = {
            "name": otp_data["name"],
            "email": otp_data["email"],
            "reg_id": notif.id,
            "user_id": notif.id,
            "site_name": "Elite Agency",
            "dashboard_url": "https://elitefreelancers.org/dashboard/",
            "created_at": timezone.now().strftime("%B %d, %Y"),
            "phone": "",
            "expertise": otp_data.get("expertise"),
            "location": "",
            "map_url": "",
        }

        def worker():
            success = send_html_email(
                otp_data["email"],
                context,
                user_type="professional"
            )
            notif.status = "SENT" if success else "FAILED"
            notif.save()

        threading.Thread(target=worker, daemon=True).start()

        return Response({
            "status": "Professional verified. Welcome email is being sent."
        }, status=200)


class ForgotPasswordRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No user found with this email"}, status=404)

        otp_code = generate_otp()
        reference_id = f"reset_{email}"

        cache.set(
            reference_id,
            {
                "email": email,
                "otp_code": otp_code,
                "is_verified": False,
            },
            timeout=600,
        )

        context = {
            "site_name": "Elite Agency",
            "site_domain": "elitefreelancer.org",
            "reference_id": reference_id,
            "otp_code": otp_code,
            "expires_in": 10,
            "email": email,
            "verification_url": "http://127.0.0.1:8000/reset-password-page/",
            "support_phone": "+977-9800000000",
        }

        success = send_forgot_password_email(email, context)

        return Response({
            "status": "Password reset OTP sent" if success else "Failed to send password reset email",
            "reference_id": reference_id,
        }, status=200 if success else 500)


class VerifyForgotPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reference_id = request.data.get("reference_id")
        otp_code = request.data.get("otp_code")

        if not reference_id or not otp_code:
            return Response({
                "error": "reference_id and otp_code are required"
            }, status=400)

        otp_data = cache.get(reference_id)

        if not otp_data:
            return Response({"error": "OTP expired or invalid"}, status=400)

        if otp_data["otp_code"] != str(otp_code):
            return Response({"error": "Invalid OTP"}, status=400)

        otp_data["is_verified"] = True
        cache.set(reference_id, otp_data, timeout=600)

        return Response({
            "status": "OTP verified. You can reset password now."
        }, status=200)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reference_id = request.data.get("reference_id")
        new_password = request.data.get("new_password")

        if not reference_id or not new_password:
            return Response({
                "error": "reference_id and new_password are required"
            }, status=400)

        otp_data = cache.get(reference_id)

        if not otp_data:
            return Response({"error": "OTP expired or invalid"}, status=400)

        if not otp_data.get("is_verified"):
            return Response({"error": "OTP not verified"}, status=400)

        try:
            user = User.objects.get(email=otp_data["email"])
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.password = make_password(new_password)
        user.save()

        cache.delete(reference_id)

        return Response({"status": "Password reset successful"}, status=200)


class BookingVerificationRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        customer_name = data.get("customer_name", "Customer")
        customer_email = data.get("email")
        service_type = data.get("service_type", "Service Booking")
        event_date = data.get("event_date", "")

        if not customer_email:
            return Response({"error": "Email is required"}, status=400)

        otp_code = generate_otp()
        reference_id = f"booking_{customer_email}"

        cache.set(
            reference_id,
            {
                "customer_name": customer_name,
                "email": customer_email,
                "service_type": service_type,
                "event_date": event_date,
                "otp_code": otp_code,
            },
            timeout=600,
        )

        context = {
            "site_name": "Elite Agency",
            "site_domain": "elitefreelancer.org",
            "reference_id": reference_id,
            "otp_code": otp_code,
            "expires_in": 10,
            "service_type": service_type,
            "customer_name": customer_name,
            "event_date": event_date,
            "verification_url": "http://127.0.0.1:8000/booking/verify/",
            "support_phone": "+977-9800000000",
        }

        def worker():
            send_booking_verification_email(customer_email, context)

        threading.Thread(target=worker, daemon=True).start()

        return Response({
            "status": "Booking verification OTP is being sent",
            "reference_id": reference_id,
        }, status=202)


class BookingVerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reference_id = request.data.get("reference_id")
        otp_code = request.data.get("otp_code")

        if not reference_id or not otp_code:
            return Response({
                "error": "reference_id and otp_code are required"
            }, status=400)

        otp_data = cache.get(reference_id)

        if not otp_data:
            return Response({"error": "OTP expired or invalid"}, status=400)

        if otp_data["otp_code"] != str(otp_code):
            return Response({"error": "Invalid OTP"}, status=400)

        cache.delete(reference_id)

        Booking.objects.create(
            user=otp_data["customer_name"],
            email=otp_data["email"],
            message=f"Booking verified for {otp_data['service_type']}",
            status="VERIFIED",
        )

        return Response({
            "status": "Booking verified successfully",
            "booking": {
                "customer_name": otp_data["customer_name"],
                "email": otp_data["email"],
                "service_type": otp_data["service_type"],
                "event_date": otp_data.get("event_date", ""),
            }
        }, status=200)


class InAppNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user_name = data.get("name", "User")
        user_email = data.get("email")
        message = data.get("message")

        if not message:
            return Response({"error": "Message is required"}, status=400)

        notif = Inapp.objects.create(
            user=user_name,
            email=user_email,
            message=message,
            status="UNREAD",
        )

        return Response({
            "status": "In-app notification saved",
            "id": notif.id,
            "user": notif.user,
            "email": notif.email,
            "message": notif.message,
        }, status=201)


class SavePushTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        token = data.get("token")
        email = data.get("email")
        user_name = data.get("name", "User")
        platform = data.get("platform", "android")

        if not token:
            return Response({"error": "FCM token is required"}, status=400)

        PushToken.objects.update_or_create(
            token=token,
            defaults={
                "user": user_name,
                "email": email,
                "platform": platform,
            }
        )

        return Response({"status": "Push token saved"}, status=201)


class SendPushView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get("email")
        title = request.data.get("title", "Elite Agency")
        message = request.data.get("message", "You have a new notification")

        tokens = PushToken.objects.all()

        if email:
            tokens = tokens.filter(email=email)

        sent = 0
        failed = 0

        for item in tokens:
            try:
                send_fcm_push(
                    token=item.token,
                    title=title,
                    body=message,
                    data={
                        "email": item.email or "",
                        "type": "push",
                    }
                )
                sent += 1
            except Exception as e:
                print("Push error:", e)
                failed += 1

        return Response({
            "status": "Push notification processed",
            "sent": sent,
            "failed": failed,
        })