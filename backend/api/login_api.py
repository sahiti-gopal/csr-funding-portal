"""Minimal env-backed login API. Run with: python3 api/login_api.py"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from dotenv import load_dotenv

load_dotenv()

HOST = "127.0.0.1"
PORT = 8000


def load_credentials():
    return {
        "email": os.getenv("LOGIN_API_EMAIL"),
        "password": os.getenv("LOGIN_API_PASSWORD"),
    }


class LoginHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/login":
            self.send_json(404, {"message": "Route not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            request_data = json.loads(self.rfile.read(content_length))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"message": "Request body must be valid JSON"})
            return

        email = request_data.get("email")
        password = request_data.get("password")
        if not email or not password:
            self.send_json(400, {"message": "Email and password are required"})
            return

        credentials = load_credentials()
        if email == credentials["email"] and password == credentials["password"]:
            self.send_json(200, {"message": "Login successful"})
        else:
            self.send_json(401, {"message": "Invalid email or password"})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    print(f"Login API running at http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), LoginHandler).serve_forever()
