import requests
import sys
import json

# Django defaults to port 8000. 
# Make sure this matches the path in your urls.py exactly.
URL = "http://127.0.0.1:8000/notify"

# This MUST match the MY_SECRET_API_KEY in your .env file
HEADERS = {
    "X-API-KEY": "furba",
    "Content-Type": "application/json"
}

# Get name and email from terminal, or use defaults
# Usage: python tests/signup.py "Your Name" "your@email.com"
name = sys.argv[1] if len(sys.argv) > 1 else "Furba User"
email = sys.argv[2] if len(sys.argv) > 2 else "chhring222@gmail.com"

payload = {
    "name": name,
    "email": email,
    "type": "MAIL"
}

def run_test():
    try:
        print(f"🚀 Triggering signup notification for: {name} ({email})")
        
        # We use json=payload which automatically sets Content-Type and serializes the dict
        response = requests.post(URL, headers=HEADERS, json=payload, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 202:
            print("✅ SUCCESS: The notification system has queued the welcome email!")
            print(f"📝 Server Response: {response.json()}")
        elif response.status_code == 401 or response.status_code == 403:
            print("❌ UNAUTHORIZED: Your X-API-KEY is incorrect.")
        elif response.status_code == 404:
            print(f"❌ NOT FOUND: The URL {URL} is incorrect. Check your urls.py.")
        else:
            print(f"⚠️ SERVER ERROR: {response.text}")

    except requests.exceptions.ConnectionError:
        print("🛑 CONNECTION ERROR: Is your Django server running? Run 'python manage.py runserver'")
    except Exception as e:
        print(f"❓ AN UNKNOWN ERROR OCCURRED: {e}")

if __name__ == "__main__":
    run_test()