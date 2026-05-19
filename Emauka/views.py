import threading

from Elite_freelancer.utils import send_html_email

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Mail, Inapp

class EmaukaMailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        user_name = data.get("name", "User")
        user_email = data.get("email")
        message = data.get("message", "Welcome to Emauka")

        if not user_email:
            return Response({"error": "Email is required"}, status=400)

        mail = Mail.objects.create(
            user=user_name,
            email=user_email,
            message=message,
            status="PENDING",
        )

        context = {
            "name": user_name,
            "email": user_email,
            "user_id": mail.id,
            "reg_id": mail.id,
            "site_name": "Emauka",
            "login_url": "https://emauka.com/login",
            "dashboard_url": "https://emauka.com/dashboard",
            "phone": data.get("phone"),
            "expertise": data.get("expertise"),
            "location": data.get("location"),
            "map_url": data.get("map_url"),
        }

        def worker():
            success = send_html_email(user_email, context, user_type="normal")
            mail.status = "SENT" if success else "FAILED"
            mail.save()

        threading.Thread(target=worker, daemon=True).start()

        return Response({
            "status": "Emauka mail is being sent",
            "id": mail.id,
            "user": mail.user,
            "email": mail.email,
            "message": mail.message,
        }, status=202)
        
class EmaukaInappView(APIView):
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
            "status": "Emauka inapp saved",
            "id": notif.id,
            "user": notif.user,
            "email": notif.email,
            "message": notif.message,
        }, status=201)

class EmaukaInappListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.GET.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        notifications = Inapp.objects.filter(
            email=email,
            status="UNREAD"
        ).order_by("-created_at")[:10]

        return Response({
            "notifications": [
                {
                    "id": n.id,
                    "message": n.message,
                    "status": n.status,
                    "is_read": n.status == "READ",
                    "created_at": n.created_at.isoformat(),
                }
                for n in notifications
            ]
        }, status=200)

class EmaukaBroadcastInappView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message")
        users = request.data.get("users", [])

        if not message:
            return Response({"error": "Message is required"}, status=400)

        if not users:
            return Response({"error": "Users list is required"}, status=400)

        created = 0

        for user in users:
            name = user.get("name", "User")
            email = user.get("email")

            if not email:
                continue

            Inapp.objects.create(
                user=name,
                email=email,
                message=message,
                status="UNREAD",
            )
            created += 1

        return Response({
            "status": "Broadcast notification created",
            "created": created,
        }, status=201)