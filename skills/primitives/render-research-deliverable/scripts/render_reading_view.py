#!/usr/bin/env python3
"""Render a local, dependency-free reading companion from explicitly supplied data."""
from __future__ import annotations

import argparse
import base64
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
import difflib
import hashlib
import html
import json
import math
from pathlib import Path
import re
from urllib.parse import urlsplit


def text(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text")
    return value


def safe_source_url(value: object) -> str:
    url = text(value, "source.url")
    parts = urlsplit(url)
    if parts.scheme not in {"https", "http"} or not parts.hostname or parts.username or parts.password:
        raise ValueError("source.url must be an HTTP(S) source without credentials")
    return url


def difference(before: str, after: str) -> dict[str, object]:
    if len(before) + len(after) > 40000:
        raise ValueError("revision comparison requires a bounded excerpt, not a whole large manuscript")
    left, right = [], []
    for kind, a, b, c, d in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
        if a < b:
            left.append({"kind": "same" if kind == "equal" else "delete", "text": before[a:b]})
        if c < d:
            right.append({"kind": "same" if kind == "equal" else "add", "text": after[c:d]})
    return {"before": left, "after": right, "identical": before == after}


def prepare(raw: dict[str, object]) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("input must be an object")
    title = text(raw.get("title"), "title")
    summary = text(raw.get("summary", ""), "summary")
    sources = raw.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources must contain at least one inspectable source description")
    clean_sources = []
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        clean_sources.append({"label": text(source.get("label"), "source.label"),
                              "note": text(source.get("note", ""), "source.note"),
                              "url": safe_source_url(source["url"]) if source.get("url") else None})
    table = raw.get("table")
    if not isinstance(table, dict) or not isinstance(table.get("columns"), list) or not table["columns"]:
        raise ValueError("table.columns must be a nonempty list")
    rows = table.get("rows")
    if not isinstance(rows, list):
        raise ValueError("table.rows must be a list (an empty list is allowed)")
    if len(rows) > 10000:
        raise ValueError("use a bounded table of at most 10000 rows for this local reading view")
    columns, keys = [], set()
    for col in table["columns"]:
        if not isinstance(col, dict):
            raise ValueError("each column must be an object")
        key = text(col.get("key"), "column.key")
        if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_-]*", key) or key in keys:
            raise ValueError("column keys must be unique simple identifiers")
        keys.add(key)
        kind = col.get("type", "text")
        if kind not in {"text", "number"}:
            raise ValueError("column.type must be text or number")
        unit = text(col.get("unit", ""), "column.unit")
        if kind == "number" and not unit.strip():
            raise ValueError("numeric columns require an explicit unit (or dimensionless)")
        decimals = col.get("decimals", 3)
        if isinstance(decimals, bool) or not isinstance(decimals, (int, Decimal)) or int(decimals) != decimals or not 0 <= decimals <= 8:
            raise ValueError("column.decimals must be an integer from 0 to 8")
        columns.append({"key": key, "label": text(col.get("label"), "column.label"),
                        "type": kind, "unit": unit, "decimals": int(decimals)})
    prepared_rows = []
    numeric_values: dict[str, set[Decimal]] = {c["key"]: set() for c in columns if c["type"] == "number"}
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) - keys:
            raise ValueError("rows must be objects containing only declared column keys")
        cells = {}
        for col in columns:
            value = row.get(col["key"])
            if value is None:
                cells[col["key"]] = {"raw": None, "display": "—", "missing": True}
            elif col["type"] == "text":
                cells[col["key"]] = {"raw": text(value, "text cell"), "display": value, "missing": False}
            else:
                if isinstance(value, bool):
                    raise ValueError("boolean is not a numeric observation")
                try:
                    number = Decimal(str(value))
                except (InvalidOperation, ValueError):
                    raise ValueError("numeric cells must be finite numbers or null") from None
                if not number.is_finite() or not math.isfinite(float(number)):
                    raise ValueError("numeric cells must be finite numbers or null")
                with localcontext() as ctx:
                    ctx.prec = max(40, len(number.as_tuple().digits) + abs(number.adjusted()) + 12)
                    shown = format(number.quantize(Decimal(1).scaleb(-col["decimals"]), rounding=ROUND_HALF_UP), "f")
                cells[col["key"]] = {"raw": str(value), "display": shown, "numeric": float(number), "missing": False}
                numeric_values[col["key"]].add(number)
        prepared_rows.append({"index": index, "cells": cells})
    # Exact-decimal ranks make sorting independent of rounded labels and JS's
    # binary precision. Plot geometry remains a visual approximation.
    for key, values in numeric_values.items():
        ranks = {value: i for i, value in enumerate(sorted(values))}
        for row in prepared_rows:
            cell = row["cells"][key]
            if not cell["missing"]:
                cell["rank"] = ranks[Decimal(cell["raw"])]
    chart = raw.get("chart")
    if chart is not None:
        if not isinstance(chart, dict) or chart.get("label_key") not in keys or chart.get("value_key") not in numeric_values:
            raise ValueError("chart must name an existing label column and numeric value column")
        chart = {"label_key": chart["label_key"], "value_key": chart["value_key"],
                 "title": text(chart.get("title"), "chart.title")}
    excerpt = raw.get("excerpt")
    if excerpt is not None:
        if not isinstance(excerpt, dict) or not isinstance(excerpt.get("highlights", []), list):
            raise ValueError("excerpt must contain text and optional highlight strings")
        excerpt = {"title": text(excerpt.get("title"), "excerpt.title"),
                   "text": text(excerpt.get("text"), "excerpt.text"),
                   "highlights": [text(x, "highlight") for x in excerpt.get("highlights", []) if x]}
    revision = raw.get("revision")
    if revision is not None:
        if not isinstance(revision, dict) or not all(isinstance(revision.get(k), str) for k in ("before", "after")):
            raise ValueError("revision requires both actual before and after texts")
        revision = {"title": text(revision.get("title", "修訂對照"), "revision.title"),
                    **difference(revision["before"], revision["after"])}
    return {"title": title, "summary": summary, "sources": clean_sources,
            "table_title": text(table.get("title", title), "table.title"), "columns": columns,
            "rows": prepared_rows, "chart": chart, "excerpt": excerpt, "revision": revision}


def render(raw: dict[str, object]) -> str:
    payload = prepare(raw)
    template = (Path(__file__).resolve().parents[1] / "assets/reading-view.html").read_text(encoding="utf-8")
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    encoded = encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    result = template.replace("__PAGE_TITLE__", html.escape(payload["title"], quote=True)).replace("__READING_DATA__", encoded)
    for tag, marker in (("style", "__STYLE_HASH__"), ("script", "__SCRIPT_HASH__")):
        pattern = r"<style>(.*?)</style>" if tag == "style" else r'<script id="reading-app">(.*?)</script>'
        code = re.search(pattern, result, re.DOTALL).group(1)
        digest = base64.b64encode(hashlib.sha256(code.encode("utf-8")).digest()).decode("ascii")
        result = result.replace(marker, digest, 1)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.suffix.lower() != ".html":
            raise ValueError("output must have .html suffix")
        raw = json.loads(args.input.read_text(encoding="utf-8-sig"), parse_float=Decimal, parse_int=Decimal)
        page = render(raw)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(page)
        print(json.dumps({"output": str(args.output.resolve()), "bytes": args.output.stat().st_size,
                          "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, InvalidOperation) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
