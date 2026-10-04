from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os


cities = {
    "almaty": "Almaty is the largest city in Kazakhstan.",
    "astana": "Astana is the capital of Kazakhstan.",
    "shymkent": "Shymkent is one of the oldest cities in Kazakhstan.",
    "london": "London is the capital of the United Kingdom.",
    "tokyo": "Tokyo is the capital of Japan."
}


class RequestHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        response = json.dumps(data).encode()

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {
                "message": "City Facts API"
            })

        elif self.path == "/healthz":
            self.send_json(200, {
                "status": "ok"
            })

        elif self.path.startswith("/city/"):
            city_name = self.path[6:].lower()

            if city_name not in cities:
                self.send_json(404, {
                    "error": "City not found"
                })
                return

            self.send_json(200, {
                "city": city_name.title(),
                "fact": cities[city_name]
            })

        else:
            self.send_json(404, {
                "error": "Not found"
            })


port = int(os.environ.get("PORT", 8080))

server = HTTPServer(("0.0.0.0", port), RequestHandler)

print(f"Server running on port {port}")

server.serve_forever()