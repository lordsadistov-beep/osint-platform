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

# Check existing services
status, services = api("GET", "/services")
print("Existing services:")
if isinstance(services, list):
    for s in services:
        print(f"  {s.get('id')} {s.get('name')} type={s.get('type')}")
else:
    print(f"  {json.dumps(services, indent=2)}")

print()

# Get static site info for ownerId
status, fe = api("GET", "/services/srv-d8nf52btqb8s73d4cgeg")
print(f"\nStatic site ownerId: {fe.get('ownerId', '?')}")

# 3. Get owners
status, owners = api("GET", "/owners")
print(f"\nOwners: {json.dumps(owners, indent=2)}")

# Use first owner's id
if isinstance(owners, list) and owners:
    owner_id = owners[0]["id"]
    print(f"\nUsing ownerId: {owner_id}")
else:
    owner_id = fe.get("ownerId")
    print(f"\nUsing fallback ownerId: {owner_id}")

# 4. Create web service
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
