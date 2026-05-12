import threading

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import NotificationHistory
from .utils import send_real_email


class NotifyView(APIView):
    def post(self, request):
        # 1. Security check
        if request.headers.get("X-API-KEY") != "furba":
            return Response({"error": "Unauthorized"}, status=401)

        data = request.data

        recipient_name = data.get("user")
        message = data.get("message")
        notify_type = data.get("type", "both")
        email = data.get("email")

        # 2. Basic validation
        if not recipient_name:
            return Response({"error": "User name is required"}, status=400)

        if not message:
            return Response({"error": "Message is required"}, status=400)

        if notify_type in ["email", "both"] and not email:
            return Response({"error": "Email is required for email notification"}, status=400)

        # 3. Save notification to database
        notif = NotificationHistory.objects.create(
            recipient_name=recipient_name,
            message=message,
            notify_type=notify_type,
            status="PENDING",
        )

        # 4. Background worker
        def worker_task(obj_id, email_address):
            obj = NotificationHistory.objects.get(id=obj_id)

            try:
                success = False

                if obj.notify_type in ["email", "both"]:
                    success = send_real_email(email_address, obj.message)

                # If type is not email/both, mark as sent for now
                if obj.notify_type not in ["email", "both"]:
                    success = True

                obj.status = "SENT" if success else "FAILED"
                obj.save()

            except Exception as e:
                obj.status = "FAILED"
                obj.save()
                print("Notification error:", e)

        threading.Thread(
            target=worker_task,
            args=(notif.id, email),
            daemon=True
        ).start()

        return Response(
            {
                "status": "processing",
                "id": notif.id,
                "message": "Notification saved and sending started",
            },
            status=202
        )