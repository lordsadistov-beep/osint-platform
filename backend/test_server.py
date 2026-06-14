import http.server, os, sys

port = int(os.environ.get("PORT", 8000))
print(f"Starting test server on port {port}", flush=True)
http.server.HTTPServer(("0.0.0.0", port), http.server.SimpleHTTPRequestHandler).serve_forever()
