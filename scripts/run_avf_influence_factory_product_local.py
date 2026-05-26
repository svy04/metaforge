from __future__ import annotations

import argparse
import http.server
import socketserver
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
INDEX = APP_DIR / "index.html"


def check() -> int:
    required = [
        INDEX,
        APP_DIR / "app.js",
        APP_DIR / "styles.css",
        APP_DIR / "PRODUCT_MANUAL.md",
        APP_DIR / "demo_workspace_v9.json",
        APP_DIR / "backup_schema_v9.json",
        APP_DIR / "local_product_manifest_v9.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        print("LOCAL_PRODUCT_LAUNCHER_CHECK=FAIL")
        for path in missing:
            print(f"missing={path}")
        return 1
    print("LOCAL_PRODUCT_LAUNCHER_CHECK=PASS")
    print(f"entrypoint={INDEX}")
    print("protected_action_executed=false")
    return 0


def serve(port: int) -> int:
    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = str(APP_DIR)
    with socketserver.TCPServer(("127.0.0.1", port), lambda *args, **kwargs: handler(*args, directory=str(APP_DIR), **kwargs)) as server:
        print(f"serving=127.0.0.1:{port}")
        print("protected_action_executed=false")
        server.serve_forever()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    if args.check:
        return check()
    if args.serve:
        return serve(args.port)
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
