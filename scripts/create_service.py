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
if isinstance(owners, list) and owners:
    entry = owners[0]
    owner_id = entry.get("owner", entry).get("id") if "owner" in entry else entry.get("id")
else:
    owner_id = owners.get("id") if isinstance(owners, dict) else None
print(f"ownerId: {owner_id}")

# Try WITHOUT runtime/env field - maybe serviceDetails is enough
payload = {
    "type": "web_service",
    "name": "osint-platform-api",
    "ownerId": owner_id,
    "plan": "free",
    "region": "oregon",
    "repo": "https://github.com/lordsadistov-beep/osint-platform",
    "autoDeploy": "yes",
    "branch": "master",
    "rootDir": "backend",
    "serviceDetails": {
        "env": "python",
        "healthCheckPath": "/health",
        "envSpecificDetails": {
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
        }
    }
}
status, result = api("POST", "/services", payload)
print(f"Try 1 (env in serviceDetails) HTTP {status}: {json.dumps(result, indent=2)}")
if status == 201:
    print(f"SUCCESS! New service ID: {result.get('id')}")
    raise SystemExit(0)

# Try with env AND runtime both as top-level
payload2 = {
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
    "serviceDetails": {
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
        "healthCheckPath": "/health"
    }
}
status, result = api("POST", "/services", payload2)
print(f"Try 2 (env top-level, flat serviceDetails) HTTP {status}: {json.dumps(result, indent=2)}")
if status == 201:
    print(f"SUCCESS! New service ID: {result.get('id')}")
    raise SystemExit(0)

# Try with env inside serviceDetails as runtime field
payload3 = {
    "type": "web_service",
    "name": "osint-platform-api",
    "ownerId": owner_id,
    "plan": "free",
    "region": "oregon",
    "repo": "https://github.com/lordsadistov-beep/osint-platform",
    "autoDeploy": "yes",
    "branch": "master",
    "rootDir": "backend",
    "serviceDetails": {
        "runtime": "python",
        "healthCheckPath": "/health",
        "envSpecificDetails": {
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
        }
    }
}
status, result = api("POST", "/services", payload3)
print(f"Try 3 (runtime in serviceDetails) HTTP {status}: {json.dumps(result, indent=2)}")
if status == 201:
    print(f"SUCCESS! New service ID: {result.get('id')}")
else:
    print("ALL FAILED")
