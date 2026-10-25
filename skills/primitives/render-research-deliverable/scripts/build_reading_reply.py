#!/usr/bin/env python3
"""Build a truthful local delivery reply only after its reading artifact exists."""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import http.client
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


def inspect_artifact(artifact: Path) -> tuple[bytes, dict[str, object]]:
    content = artifact.read_bytes()
    match = re.search(r'<script type="application/json" id="reading-data">(.*?)</script>', content.decode("utf-8"), re.DOTALL)
    if not match:
        raise ValueError("artifact is not an inspectable reading view")
    payload = json.loads(match.group(1))
    if not isinstance(payload.get("title"), str) or not isinstance(payload.get("summary"), str):
        raise ValueError("reading artifact lacks its title or summary")
    return content, payload


def verified_target(artifact: Path, content: bytes, url: str | None) -> tuple[str, str]:
    if not url:
        target = artifact.resolve().as_posix()
        return target, "此連結僅適用於儲存這份檔案的電腦。"
    parts = urlsplit(url)
    if parts.scheme != "http" or parts.hostname not in {"127.0.0.1", "localhost", "::1"} or parts.username or parts.password:
        raise ValueError("only an explicit local loopback HTTP URL is supported; no public hosting is performed")
    # Direct HTTPConnection avoids proxy environment routing. No arbitrary
    # remote host, redirects, authentication, or signed URL is followed.
    connection = http.client.HTTPConnection(parts.hostname, parts.port, timeout=5)
    try:
        connection.request("GET", (parts.path or "/") + ("?" + parts.query if parts.query else ""))
        response = connection.getresponse()
        received = response.read(len(content) + 1)
        if response.status != 200 or received != content:
            raise ValueError("link does not return the exact generated artifact")
    finally:
        connection.close()
    return url, "此連結僅供這台電腦的瀏覽器開啟；沒有公開到網路。"


def markdown_label(value: str) -> str:
    return re.sub(r"([\\\[\]])", r"\\\1", value.replace("\n", " "))


def build_reply(artifact: Path, next_step: str, url: str | None = None) -> dict[str, str]:
    if not next_step.strip():
        raise ValueError("an actionable next step is required")
    content, payload = inspect_artifact(artifact)
    target, scope = verified_target(artifact, content, url)
    title = str(payload["title"])
    # Escape URL delimiter characters in local path targets without pretending
    # a Windows path is an Internet URL.
    link_target = target.replace("<", "%3C").replace(">", "%3E").replace("\n", "%0A")
    markdown = f'{payload["summary"]}\n\n[開啟：{markdown_label(title)}](<{link_target}>)\n\n{scope}\n\n下一步：{next_step}\n'
    response_html = '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; base-uri \'none\'"><title>本次助理回覆</title></head><body><main><h1>本次助理回覆</h1><p>'+html.escape(str(payload['summary']))+'</p><p><a href="'+html.escape(target,quote=True)+'">'+html.escape('開啟：'+title)+'</a></p><p>'+html.escape(scope)+'</p><p>下一步：'+html.escape(next_step)+'</p></main></body></html>'
    css='body{max-width:850px;margin:35px auto;padding:22px;font:20px/1.8 system-ui,sans-serif;color:#18353e;background:#f3f6f2}h1{font-size:28px}p{white-space:pre-line}a{display:inline-block;padding:12px 20px;background:#176f63;color:white;border-radius:8px;text-underline-offset:4px}@media(max-width:600px){body{margin:12px auto;font-size:18px;padding:16px}}'
    digest=base64.b64encode(hashlib.sha256(css.encode()).digest()).decode()
    response_html=response_html.replace("default-src 'none'; base-uri", "default-src 'none'; style-src 'sha256-"+digest+"'; base-uri").replace('</head>','<style>'+css+'</style></head>')
    return {"markdown": markdown, "response_html": response_html, "target": target, "scope": scope,
            "sha256": hashlib.sha256(content).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", required=True, type=Path)
    parser.add_argument("--next-step", required=True)
    parser.add_argument("--url", help="Optional loopback URL; fetched and byte-checked before use")
    parser.add_argument("--output", required=True, type=Path, help="Markdown reply; never overwrites")
    parser.add_argument("--response-html", type=Path, help="Optional readable copy of the same reply, with a real anchor")
    args = parser.parse_args()
    try:
        targets = [args.output] + ([args.response_html] if args.response_html else [])
        if len({p.resolve() for p in targets}) != len(targets) or any(p.exists() for p in targets):
            raise FileExistsError("reply output already exists or aliases another output")
        result = build_reply(args.artifact, args.next_step, args.url)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(result["markdown"])
        if args.response_html:
            args.response_html.parent.mkdir(parents=True, exist_ok=True)
            with args.response_html.open("x", encoding="utf-8") as handle:
                handle.write(result["response_html"])
        print(json.dumps({"status": "ready", "reply": str(args.output.resolve()), "target": result["target"],
                          "artifact_sha256": result["sha256"], "scope": result["scope"]}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, http.client.HTTPException) as exc:
        print(json.dumps({"status": "not_ready", "error": str(exc), "usable_link": False}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
