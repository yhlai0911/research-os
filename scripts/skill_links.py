"""Resolve packaged Markdown dependencies and rebase bucketed source links."""
from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

LINK = re.compile(r'\[[^\]]*\]\((?P<target><[^>]+>|[^\s)]+)(?:\s+"[^"\n]*")?\)')
REFERENCE = re.compile(r'^\s{0,3}\[[^\]]+\]:\s*(?P<target><[^>]+>|\S+)', re.M)


def local_links(text: str):
    for pattern in (LINK, REFERENCE):
        for match in pattern.finditer(text):
            href = match['target'].strip('<>')
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            yield match, unquote(parts.path), href[len(parts.path):]


def owner(path: Path, roots: list[Path]) -> Path | None:
    path = path.resolve()
    return next((root for root in roots if path.is_relative_to(root.resolve())), None)


def rebase_markdown(text: str, file: Path, roots: list[Path]) -> str:
    origin = owner(file, roots)
    if origin is None:
        return text
    changes = []
    for match, relative, suffix in local_links(text):
        resolved = (file.parent / relative).resolve()
        destination = owner(resolved, roots)
        if destination is None:
            continue
        from_dir = Path(origin.name) / file.relative_to(origin).parent
        to_file = Path(destination.name) / resolved.relative_to(destination.resolve())
        relative_target = os.path.relpath(to_file, from_dir).replace('\\', '/')
        raw = match['target']
        new = (
            '<' + relative_target + suffix + '>' if raw.startswith('<')
            else quote(relative_target, safe='/._~-') + suffix
        )
        if new != raw:
            changes.append((*match.span('target'), new))
    for start, end, new in sorted(changes, reverse=True):
        text = text[:start] + new + text[end:]
    return text


def dependency_errors(directory: Path, allowed: list[Path], fallback=None) -> list[str]:
    """Read every declared local Markdown dependency; never execute its content."""
    errors = []
    allowed = [path.resolve() for path in allowed]
    for file in sorted(directory.rglob('*.md')):
        try:
            text = file.read_text(encoding='utf-8')
        except OSError as exc:
            errors.append(f'{file}: unreadable Markdown: {exc}')
            continue
        for match, relative, _suffix in local_links(text):
            target = (file.parent / relative).resolve()
            if fallback is not None and not target.exists():
                staged, installed = fallback
                if target.is_relative_to(staged.resolve()):
                    target = installed.resolve() / target.relative_to(staged.resolve())
            location = f'{file}:{text.count(chr(10), 0, match.start()) + 1}'
            if not any(target.is_relative_to(path) for path in allowed):
                errors.append(f'{location}: dependency leaves packaged skills: {match["target"]}')
                continue
            try:
                if not target.is_file():
                    raise FileNotFoundError(str(target))
                target.read_bytes()
            except OSError as exc:
                errors.append(f'{location}: missing/unreadable dependency {match["target"]}: {exc}')
    return errors
