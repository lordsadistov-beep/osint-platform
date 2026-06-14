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

# Try 1: runtime as top-level field
payload1 = {
    "type": "web_service",
    "name": "osint-platform-api",
    "ownerId": owner_id,
    "runtime": "python",
    "plan": "free",
    "region": "oregon",
    "repo": "https://github.com/lordsadistov-beep/osint-platform",
    "autoDeploy": "yes",
    "branch": "master",
    "rootDir": "backend",
    "serviceDetails": {
        "healthCheckPath": "/health",
        "envSpecificDetails": {
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
        }
    }
}
status, result = api("POST", "/services", payload1)
print(f"Try 1 (runtime top-level) HTTP {status}: {json.dumps(result, indent=2)}")
if status == 201:
    print(f"SUCCESS! New service ID: {result.get('id')}")
else:
    # Try 2: env as top-level with serviceDetails
    payload2 = dict(payload1)
    payload2["env"] = "python"
    del payload2["runtime"]
    status, result = api("POST", "/services", payload2)
    print(f"Try 2 (env top-level) HTTP {status}: {json.dumps(result, indent=2)}")
    if status == 201:
        print(f"SUCCESS! New service ID: {result.get('id')}")
    else:
        print("ALL FAILED")
