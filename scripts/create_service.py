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
        return e.code, json.loads(e.read().decode())

# Get owners
status, owners = api("GET", "/owners")
print(f"Owners raw: {json.dumps(owners, indent=2)[:500]}")
owner_id = None
if isinstance(owners, list) and owners:
    entry = owners[0]
    if "owner" in entry:
        owner_id = entry["owner"]["id"]
    else:
        owner_id = entry.get("id")
print(f"Using ownerId: {owner_id}")

# Get static site for verification
status, fe = api("GET", "/services/srv-d8nf52btqb8s73d4cgeg")
print(f"FE ownerId: {fe.get('ownerId', fe.get('serviceDetails', {}).get('ownerId', '?'))}")

# Create web service
payload = {
    "type": "web_service",
    "name": "osint-platform-api",
    "ownerId": owner_id,
    "env": "python",
    "plan": "free",
    "region": "oregon",
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthCheckPath": "/health",
    "repo": "https://github.com/lordsadistov-beep/osint-platform",
    "autoDeploy": "yes",
    "branch": "master",
    "rootDir": "backend"
}
status, result = api("POST", "/services", payload)
print(f"\nCreate result (HTTP {status}): {json.dumps(result, indent=2)}")
if status == 201:
    new_id = result.get("id", "?")
    print(f"New service ID: {new_id}")
else:
    print("FAILED!")
