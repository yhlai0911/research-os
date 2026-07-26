#!/usr/bin/env python3
"""Atomically claim and terminally seal or release one Research OS target."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


def now() -> str:
    return datetime.now(UTC).isoformat()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def emit(payload: dict[str, object], status: int = 0) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return status


def valid_claim_id(claim_id: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9._-]+", claim_id))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def publish_json_once(
    path: Path, payload: dict[str, object]
) -> tuple[bool, dict[str, object]]:
    """Publish a complete JSON file with an atomic no-replace hard link."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.{os.getpid()}.{uuid4().hex}.tmp"
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
            return True, payload
        except FileExistsError:
            return False, read_json(path)
    finally:
        temporary.unlink(missing_ok=True)


def claim_paths(
    state_root: Path, claim_id: str
) -> tuple[Path, Path, Path, Path]:
    active = state_root / ".claims" / f"{claim_id}.claim"
    sealed = state_root / ".receipts" / f"{claim_id}.json"
    terminal = state_root / ".terminals" / f"{claim_id}.json"
    history = state_root / ".claim-history" / claim_id
    return active, sealed, terminal, history


def claim(args: argparse.Namespace) -> int:
    if not valid_claim_id(args.claim_id):
        return emit(
            {"status": "blocked", "reason": "invalid-claim-id", "claim_id": args.claim_id},
            2,
        )
    state_root = args.state_root.resolve()
    source = args.source.resolve()
    active, sealed, terminal, history = claim_paths(state_root, args.claim_id)

    if not source.is_file():
        return emit(
            {"status": "blocked", "reason": "source-not-found", "source": str(source)},
            2,
        )
    actual = digest(source)
    if actual != args.expected_sha256:
        return emit(
            {
                "status": "blocked",
                "reason": "source-hash-mismatch",
                "expected": args.expected_sha256,
                "actual": actual,
            },
            2,
        )

    if terminal.is_file():
        try:
            terminal_payload = read_json(terminal)
        except json.JSONDecodeError:
            return emit(
                {
                    "status": "blocked",
                    "reason": "terminal-receipt-invalid",
                    "terminal": str(terminal),
                },
                2,
            )
        if (
            terminal_payload.get("claim_id") != args.claim_id
            or terminal_payload.get("source_sha256") != actual
        ):
            return emit(
                {
                    "status": "blocked",
                    "reason": "terminal-version-conflict",
                    "claim_id": args.claim_id,
                    "source_sha256": actual,
                    "terminal_source_sha256": terminal_payload.get("source_sha256"),
                },
                2,
            )
        state = terminal_payload.get("terminal_state")
        return emit(
            {
                "status": f"already-{state}",
                "claim_id": args.claim_id,
                "terminal": str(terminal),
                "public_receipt": str(sealed) if state == "sealed" else str(history / "release.json"),
                "terminal_payload": terminal_payload,
            }
        )

    active.parent.mkdir(parents=True, exist_ok=True)
    try:
        active.mkdir()
    except FileExistsError:
        claim_path = active / "claim.json"
        current = (
            read_json(claim_path)
            if claim_path.is_file()
            else {"status": "claim-incomplete"}
        )
        return emit(
            {
                "status": "already-claimed",
                "claim_id": args.claim_id,
                "active_claim": str(active),
                "current": current,
            },
            3,
        )

    payload = {
        "status": "claimed",
        "claim_id": args.claim_id,
        "source": str(source),
        "source_sha256": actual,
        "owner": args.owner,
        "claimed_at": now(),
    }
    claim_path = active / "claim.json"
    try:
        published, _ = publish_json_once(claim_path, payload)
        if not published:
            raise RuntimeError("claim record unexpectedly existed in new claim directory")
    except Exception:
        active.rmdir()
        raise
    return emit({**payload, "active_claim": str(active)})


def validate_execution_receipt(
    receipt_source: Path,
    claim_id: str,
    owner: str,
    result: str,
    source_sha256: str,
) -> tuple[dict[str, object] | None, dict[str, object] | None]:
    if not receipt_source.is_file():
        return None, {
            "status": "blocked",
            "reason": "execution-receipt-not-found",
            "receipt": str(receipt_source),
        }
    try:
        execution_receipt = read_json(receipt_source)
    except json.JSONDecodeError:
        return None, {
            "status": "blocked",
            "reason": "execution-receipt-invalid-json",
            "receipt": str(receipt_source),
        }
    required = {
        "claim_id",
        "owner",
        "status",
        "source_sha256",
        "domain_verdict",
        "outputs",
        "checks",
        "readback",
    }
    missing = sorted(required - set(execution_receipt))
    if missing:
        return None, {
            "status": "blocked",
            "reason": "execution-receipt-schema-invalid",
            "missing_fields": missing,
        }
    expected = {
        "claim_id": claim_id,
        "owner": owner,
        "status": result,
        "source_sha256": source_sha256,
    }
    mismatches = {
        key: {"expected": value, "actual": execution_receipt.get(key)}
        for key, value in expected.items()
        if execution_receipt.get(key) != value
    }
    if mismatches:
        return None, {
            "status": "blocked",
            "reason": "execution-receipt-mismatch",
            "mismatches": mismatches,
        }
    if not isinstance(execution_receipt["outputs"], list) or not isinstance(
        execution_receipt["checks"], list
    ):
        return None, {
            "status": "blocked",
            "reason": "execution-receipt-schema-invalid",
            "detail": "outputs and checks must be lists",
        }
    return execution_receipt, None


def archive_active(active: Path, history: Path) -> tuple[bool, str | None]:
    history.parent.mkdir(parents=True, exist_ok=True)
    if history.exists():
        if active.exists():
            return False, "active-and-history-both-exist"
        return True, None
    if not active.exists():
        return False, "active-claim-missing"
    try:
        os.replace(active, history)
    except OSError as exc:
        return False, str(exc)
    return True, None


def seal(args: argparse.Namespace) -> int:
    if not valid_claim_id(args.claim_id):
        return emit(
            {"status": "blocked", "reason": "invalid-claim-id", "claim_id": args.claim_id},
            2,
        )
    state_root = args.state_root.resolve()
    active, sealed, terminal, history = claim_paths(state_root, args.claim_id)
    receipt_source = args.receipt.resolve()

    if terminal.is_file():
        terminal_payload = read_json(terminal)
        expected_receipt_hash = (
            digest(receipt_source) if receipt_source.is_file() else None
        )
        if (
            terminal_payload.get("terminal_state") != "sealed"
            or terminal_payload.get("owner") != args.owner
            or terminal_payload.get("status") != args.result
            or terminal_payload.get("execution_receipt_sha256")
            != expected_receipt_hash
        ):
            return emit(
                {
                    "status": "blocked",
                    "reason": "terminal-state-conflict",
                    "terminal": terminal_payload,
                },
                4,
            )
    else:
        claim_path = active / "claim.json"
        if not claim_path.is_file():
            return emit(
                {
                    "status": "blocked",
                    "reason": "active-claim-not-found",
                    "active_claim": str(active),
                },
                2,
            )
        current = read_json(claim_path)
        if current.get("owner") != args.owner:
            return emit(
                {
                    "status": "blocked",
                    "reason": "claim-owner-mismatch",
                    "expected_owner": current.get("owner"),
                    "actual_owner": args.owner,
                },
                3,
            )
        source = Path(str(current.get("source", "")))
        if not source.is_file():
            return emit(
                {
                    "status": "blocked",
                    "reason": "claimed-source-not-found",
                    "source": str(source),
                },
                2,
            )
        current_source_hash = digest(source)
        if current_source_hash != current.get("source_sha256"):
            return emit(
                {
                    "status": "blocked",
                    "reason": "claimed-source-changed",
                    "claimed_source_sha256": current.get("source_sha256"),
                    "current_source_sha256": current_source_hash,
                },
                2,
            )
        execution_receipt, receipt_error = validate_execution_receipt(
            receipt_source,
            args.claim_id,
            args.owner,
            args.result,
            current_source_hash,
        )
        if receipt_error:
            return emit(receipt_error, 2)
        terminal_payload = {
            **current,
            "status": args.result,
            "terminal_state": "sealed",
            "terminal_at": now(),
            "execution_receipt": str(receipt_source),
            "execution_receipt_sha256": digest(receipt_source),
            "domain_verdict": execution_receipt["domain_verdict"],
        }
        won, existing = publish_json_once(terminal, terminal_payload)
        if not won:
            if existing != terminal_payload:
                return emit(
                    {
                        "status": "blocked",
                        "reason": "terminal-state-conflict",
                        "terminal": existing,
                    },
                    4,
                )
            terminal_payload = existing

    published, existing_sealed = publish_json_once(sealed, terminal_payload)
    if not published and existing_sealed != terminal_payload:
        return emit(
            {
                "status": "blocked",
                "reason": "sealed-receipt-conflict",
                "receipt": str(sealed),
            },
            4,
        )
    archived, archive_error = archive_active(active, history)
    if not archived:
        return emit(
            {
                "status": "partial",
                "reason": "terminal-published-archive-incomplete",
                "terminal": str(terminal),
                "receipt": str(sealed),
                "archive_error": archive_error,
            },
            5,
        )
    return emit(
        {
            **terminal_payload,
            "terminal": str(terminal),
            "receipt": str(sealed),
            "claim_history": str(history),
        }
    )


def release(args: argparse.Namespace) -> int:
    if not valid_claim_id(args.claim_id):
        return emit(
            {"status": "blocked", "reason": "invalid-claim-id", "claim_id": args.claim_id},
            2,
        )
    state_root = args.state_root.resolve()
    active, _, terminal, history = claim_paths(state_root, args.claim_id)

    if terminal.is_file():
        terminal_payload = read_json(terminal)
        if (
            terminal_payload.get("terminal_state") != "released"
            or terminal_payload.get("owner") != args.owner
            or terminal_payload.get("release_reason") != args.reason
        ):
            return emit(
                {
                    "status": "blocked",
                    "reason": "terminal-state-conflict",
                    "terminal": terminal_payload,
                },
                4,
            )
    else:
        claim_path = active / "claim.json"
        if not claim_path.is_file():
            return emit(
                {
                    "status": "blocked",
                    "reason": "active-claim-not-found",
                    "active_claim": str(active),
                },
                2,
            )
        current = read_json(claim_path)
        if current.get("owner") != args.owner:
            return emit(
                {
                    "status": "blocked",
                    "reason": "claim-owner-mismatch",
                    "expected_owner": current.get("owner"),
                    "actual_owner": args.owner,
                },
                3,
            )
        terminal_payload = {
            **current,
            "status": "released",
            "terminal_state": "released",
            "terminal_at": now(),
            "release_reason": args.reason,
        }
        won, existing = publish_json_once(terminal, terminal_payload)
        if not won:
            if existing != terminal_payload:
                return emit(
                    {
                        "status": "blocked",
                        "reason": "terminal-state-conflict",
                        "terminal": existing,
                    },
                    4,
                )
            terminal_payload = existing

    archived, archive_error = archive_active(active, history)
    if not archived:
        return emit(
            {
                "status": "partial",
                "reason": "terminal-published-archive-incomplete",
                "terminal": str(terminal),
                "archive_error": archive_error,
            },
            5,
        )
    release_path = history / "release.json"
    published, existing_release = publish_json_once(release_path, terminal_payload)
    if not published and existing_release != terminal_payload:
        return emit(
            {
                "status": "partial",
                "reason": "release-receipt-conflict",
                "terminal": str(terminal),
                "release_receipt": str(release_path),
            },
            5,
        )
    return emit(
        {
            **terminal_payload,
            "terminal": str(terminal),
            "claim_history": str(history),
            "release_receipt": str(release_path),
        }
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)

    claim_parser = commands.add_parser("claim")
    claim_parser.add_argument("--state-root", type=Path, required=True)
    claim_parser.add_argument("--claim-id", required=True)
    claim_parser.add_argument("--source", type=Path, required=True)
    claim_parser.add_argument("--expected-sha256", required=True)
    claim_parser.add_argument("--owner", required=True)
    claim_parser.set_defaults(handler=claim)

    seal_parser = commands.add_parser("seal")
    seal_parser.add_argument("--state-root", type=Path, required=True)
    seal_parser.add_argument("--claim-id", required=True)
    seal_parser.add_argument("--owner", required=True)
    seal_parser.add_argument(
        "--result", choices=("complete", "partial", "blocked"), required=True
    )
    seal_parser.add_argument("--receipt", type=Path, required=True)
    seal_parser.set_defaults(handler=seal)

    release_parser = commands.add_parser("release")
    release_parser.add_argument("--state-root", type=Path, required=True)
    release_parser.add_argument("--claim-id", required=True)
    release_parser.add_argument("--owner", required=True)
    release_parser.add_argument("--reason", required=True)
    release_parser.set_defaults(handler=release)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
