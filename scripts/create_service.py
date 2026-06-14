import os, json, urllib.request

KEY = os.environ["RENDER_API_KEY"]
BASE = "https://api.render.com/v1"
AUTH = f"Bearer {KEY}"

def api(method, path, data=None):
    req = urllib.request.Request(f"{BASE}{path}")
    req.add_header("Authorization", AUTH)
    req.add_header("Content-Type", "application/json")
    if data:
        req.data = json.dumps(data).encode()
    req.method = method
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"raw": body}

# Get owners
status, owners = api("GET", "/owners")
owner_id = None
if isinstance(owners, list) and owners:
    entry = owners[0]
    if "owner" in entry:
        owner_id = entry["owner"]["id"]
else:
    owner_id = owners.get("id") if isinstance(owners, dict) else None
print(f"ownerId: {owner_id}")

# Create web service
payload = {
    "type": "web_service",
    "name": "osint-platform-api",
    "ownerId": owner_id,
    "env": "python",
    "plan": "free",
    "region": "oregon",
    "repo": "https://github.com/lordsadistov-beep/osint-platform",
    "autoDeploy": "yes",
    "branch": "master",
    "rootDir": "backend",
    "healthCheckPath": "/health",
    "serviceDetails": {
        "envSpecificDetails": {
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
        }
    }
}
status, result = api("POST", "/services", payload)
print(f"Create result (HTTP {status}): {json.dumps(result, indent=2)}")
if status == 201:
    new_id = result.get("id")
    print(f"New service ID: {new_id}")

    # Set env vars
    env_payload = [
        {"key": "DATABASE_URL", "value": "postgresql+asyncpg://osint_platform_y27c_user:QrtH8lM7eAH9vYgJt0LzMYyQ2X87URvo@dpg-d8nf51nlk1mc739m3g90-a:5432/osint_platform_y27c"},
        {"key": "SECRET_KEY", "value": "osint-platform-secret-key-change-in-production-2024"},
        {"key": "FRONTEND_URL", "value": "https://osint-platform-frontend.onrender.com"},
        {"key": "CORS_ORIGINS", "value": "https://osint-platform-frontend.onrender.com,http://localhost:5173"}
    ]
    es, er = api("PUT", f"/services/{new_id}/env-vars", env_payload)
    print(f"Env vars set (HTTP {es}): {json.dumps(er, indent=2)}")
else:
    print("FAILED!")
