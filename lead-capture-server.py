"""Lead capture server for activemillers.com "notify me" case study alerts.

Receives {email, source, list} from the lead-magnet form on any case study page,
appends to a local CSV, and returns 200. This is the newsletter-growth test:
subscribe to get notified when new case studies go live, real-time medicine,
in exchange for an email address.

Run: python lead-capture-server.py
Binds to 127.0.0.1:8761 only, not accessible from the network.
"""
import json
import os
import re
import csv
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_CSV = os.path.join(SITE_DIR, "leads.csv")
PDF_DIR = os.path.join(SITE_DIR, "downloads")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "leads_file": LEADS_CSV}).encode())
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path != "/subscribe":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw)
        except Exception:
            self.send_response(400)
            self._cors()
            self.end_headers()
            return

        email = (data.get("email") or "").strip().lower()
        source = (data.get("source") or "unknown").strip()
        subscribed_list = (data.get("list") or "").strip()

        if not EMAIL_RE.match(email):
            self.send_response(400)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": "invalid email"}).encode())
            return

        is_new = not os.path.exists(LEADS_CSV)
        with open(LEADS_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["timestamp_utc", "email", "source", "list"])
            writer.writerow([datetime.now(timezone.utc).isoformat(), email, source, subscribed_list])

        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode())

    def log_message(self, fmt, *args):
        print("[lead-capture]", fmt % args)


if __name__ == "__main__":
    os.makedirs(PDF_DIR, exist_ok=True)
    server = HTTPServer(("127.0.0.1", 8761), Handler)
    print(f"Lead capture server running on http://127.0.0.1:8761")
    print(f"Leads written to: {LEADS_CSV}")
    server.serve_forever()
