import json
import os
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DIRECTORY, "messages.json")


def read_messages():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def write_messages(messages):
    temporary_file = DATA_FILE + ".tmp"
    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=True, indent=2)
    os.replace(temporary_file, DATA_FILE)


class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def send_json(self, status, data):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        if self.path == "/api/messages":
            self.send_json(200, read_messages())
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/messages":
            self.send_error(404)
            return

        data = self.read_json()
        text = str(data.get("text", "")).strip()
        if not text:
            self.send_json(400, {"error": "Message cannot be empty"})
            return

        messages = read_messages()
        messages.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "x": 0,
            "y": 0
        })
        write_messages(messages)
        self.send_json(201, messages)

    def do_DELETE(self):
        if self.path == "/api/messages":
            write_messages([])
            self.send_json(200, [])
            return

        prefix = "/api/messages/"
        if self.path.startswith(prefix):
            message_id = self.path[len(prefix):]
            messages = [message for message in read_messages() if message["id"] != message_id]
            write_messages(messages)
            self.send_json(200, messages)
            return

        self.send_error(404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), AppHandler)
    print(f"Ama messages server running at http://localhost:{port}")
    server.serve_forever()
