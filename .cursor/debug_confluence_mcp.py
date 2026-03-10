#!/usr/bin/env python3
"""
One-off diagnostic: simulate Confluence MCP connection with same URL/headers as mcp.json.
Logs to .cursor/debug-5847b1.log (NDJSON) for debug session 5847b1. Do not log token value.
"""
import os
import json
import urllib.request
import urllib.error

LOG_PATH = os.path.join(os.path.dirname(__file__), "debug-5847b1.log")
CONF_URL = "https://mcp.tc.lenovo.com/confluence/mcp"
ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")

def load_env_file():
    """Load .cursor/.env into os.environ if present."""
    if not os.path.isfile(ENV_PATH):
        return
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def write_log(data: dict) -> None:
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(data) + "\n")

def main():
    load_env_file()
    token = (os.environ.get("MCP_CONF_TOKEN") or "").strip()

    # #region agent log
    write_log({
        "sessionId": "5847b1",
        "hypothesisId": "H1",
        "location": "debug_confluence_mcp.py:token_check",
        "message": "MCP_CONF_TOKEN presence and length (no value)",
        "data": {"token_set": bool(token), "token_length": len(token)},
        "timestamp": __import__("time").time() * 1000,
    })
    # #endregion

    if not token:
        write_log({
            "sessionId": "5847b1",
            "hypothesisId": "H1",
            "location": "debug_confluence_mcp.py:no_token",
            "message": "Token empty; cannot send request",
            "data": {},
            "timestamp": __import__("time").time() * 1000,
        })
        return

    req = urllib.request.Request(
        CONF_URL,
        headers={"X-Confluence-Authorization": f"Token {token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            status = r.getcode()
            body = r.read().decode("utf-8", errors="replace")[:500]
    except urllib.error.HTTPError as e:
        status = e.code
        body = (e.read().decode("utf-8", errors="replace") if e.fp else "")[:500]
    except Exception as e:
        status = -1
        body = str(e)[:500]

    # #region agent log
    write_log({
        "sessionId": "5847b1",
        "hypothesisId": "H3,H4,H5",
        "location": "debug_confluence_mcp.py:response",
        "message": "Confluence MCP response status and body preview",
        "data": {"status": status, "body_preview": body, "header_used": "X-Confluence-Authorization: Token <redacted>"},
        "timestamp": __import__("time").time() * 1000,
    })
    # #endregion

if __name__ == "__main__":
    main()
