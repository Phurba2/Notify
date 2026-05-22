import sys
import requests

URL = "http://127.0.0.1:8000/notify"

name = sys.argv[1] if len(sys.argv) > 1 else "Furba"
email = sys.argv[2] if len(sys.argv) > 2 else "chhring222@gmail.com"

payload = {
    "name": name,
    "email": email,
    "type": "Mail",
}

headers = {
    "X-API-KEY": "furba",
}

try:
    print(f"Triggering signup notification for: {name} ({email})")

    response = requests.post(URL, headers=headers, json=payload, timeout=10)

    print("Status Code:", response.status_code)

    if response.status_code == 202:
        print("SUCCESS: Welcome email queued.")
        print(response.json())
    elif response.status_code in [401, 403]:
        print("UNAUTHORIZED: API key is incorrect.")
    elif response.status_code == 404:
        print("NOT FOUND: Check your URL in urls.py.")
    else:
        print("SERVER ERROR:", response.text)

except requests.exceptions.ConnectionError:
    print("CONNECTION ERROR: Run 'python manage.py runserver' first.")
except Exception as e:
    print("UNKNOWN ERROR:", e)