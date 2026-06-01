from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

# Ensure os is imported if Phase 12 uses os.getenv.
if "os.getenv" in s and "import os\n" not in s[:500]:
    s = "import os\n" + s

# Ensure FastAPI Request is imported.
if "Request" in s and "from fastapi import Request" not in s:
    lines = s.splitlines()
    changed = False
    for i, line in enumerate(lines):
        if line.startswith("from fastapi import "):
            imports = [item.strip() for item in line.replace("from fastapi import ", "").split(",")]
            if "Request" not in imports:
                imports.append("Request")
                lines[i] = "from fastapi import " + ", ".join(imports)
            changed = True
            break

    if not changed:
        lines.insert(0, "from fastapi import Request")

    s = "\n".join(lines) + "\n"

# Ensure CORS middleware import exists if used.
if "CORSMiddleware" in s and "from fastapi.middleware.cors import CORSMiddleware" not in s:
    lines = s.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("from fastapi import "):
            insert_at = i + 1
            break
    lines.insert(insert_at, "from fastapi.middleware.cors import CORSMiddleware")
    s = "\n".join(lines) + "\n"

p.write_text(s)
print("Phase 12 backend import repair applied")
