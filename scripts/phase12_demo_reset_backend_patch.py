from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

if "import os" not in s:
    s = "import os\n" + s

if "from fastapi.middleware.cors import CORSMiddleware" not in s:
    s = s.replace(
        "from fastapi import FastAPI, HTTPException",
        "from fastapi import FastAPI, HTTPException, Request\nfrom fastapi.middleware.cors import CORSMiddleware"
    )

if "CORS_ORIGINS =" not in s:
    app_pos = s.index("app = FastAPI(")
    end_pos = s.index("\n)\n", app_pos) + len("\n)\n")
    cors_block = '''
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "X-Demo-Reset-Token"],
)
'''
    s = s[:end_pos] + cors_block + s[end_pos:]

if "class DemoResetResult" not in s:
    marker = "\n\nclass MCPRequestRecord"
    replacement = '''


class DemoResetResult(BaseModel):
    status: str
    reset_records: int
    message: str


class MCPRequestRecord'''
    if marker not in s:
        raise SystemExit("MCPRequestRecord marker not found")
    s = s.replace(marker, replacement, 1)

if "/api/demo/reset" not in s:
    marker = '@app.get("/api/dashboard", response_model=DashboardSummary)'
    reset_endpoint = '''@app.post("/api/demo/reset", response_model=DemoResetResult)
def demo_reset(request: Request):
    expected_token = os.getenv("DEMO_RESET_TOKEN")
    provided_token = request.headers.get("X-Demo-Reset-Token")

    if not expected_token:
        raise HTTPException(status_code=403, detail="Demo reset token is not configured")

    if provided_token != expected_token:
        raise HTTPException(status_code=403, detail="Invalid demo reset token")

    REQUESTS.clear()
    seed()

    return DemoResetResult(
        status="reset",
        reset_records=len(REQUESTS),
        message="Seeded MCP governance demo records restored",
    )


'''
    if marker not in s:
        raise SystemExit("dashboard endpoint marker not found")
    s = s.replace(marker, reset_endpoint + marker)

p.write_text(s)
print("Phase 12 backend demo reset patch applied")
