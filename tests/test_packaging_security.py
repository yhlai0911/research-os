from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import zipfile
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "package_release.py"
spec = importlib.util.spec_from_file_location("packaging_security_subject", SCRIPT)
packaging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packaging)


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args],
        env={**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull},
        text=True,
        stderr=subprocess.PIPE,
    ).rstrip("\n")


def write(root: Path, name: str, data: str = "fixture content\n") -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")
    return path


def commit(root: Path) -> None:
    git(root, "add", "--force", "--all")
    git(root, "commit", "--quiet", "-m", "test fixture")


@pytest.fixture
def repository(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "--quiet", "--template=")
    git(root, "config", "user.name", "Packaging tests")
    git(root, "config", "user.email", "packaging-tests@example.invalid")
    write(root, ".gitignore", "dist/\n.env\n.local-cache/\n")
    write(root, "README.md")
    write(root, "skills/catalog.yaml", 'version: "2.0.0"\n')
    commit(root)
    monkeypatch.setattr(packaging, "ROOT", root)
    return root


def names(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in packaging.source_files()}


@pytest.mark.parametrize(
    "name",
    [
        ".env", "nested/.env.production", "dist/.env", "certs/PRIVATE.KEY",
        "keys/id_ecdsa", "keys/id_ed25519", "certificate.P12", "credentials-prod.json",
        "service-account-prod.json", "service_account_prod.json", "nested/.netrc",
        "nested/.npmrc", ".pypirc", ".aws/config", ".ssh/config", ".kube/config",
        "nested/.env.directory/settings.txt",
    ],
)
def test_force_tracked_credentials_fail_closed_without_content(
    repository: Path, name: str,
) -> None:
    marker = "private-fixture-must-never-appear-in-diagnostics"
    write(repository, name, marker)
    commit(repository)
    with pytest.raises(RuntimeError, match="look like credentials") as exc:
        packaging.source_files()
    assert name in str(exc.value)
    assert marker not in str(exc.value)


def test_inventory_excludes_tracked_ignored_files_and_build_artifacts(repository: Path) -> None:
    excluded = {
        "dist/old.zip", ".local-cache/data.txt", "nested/renders/frame.png",
        "nested/.venv/bin/python", "nested/__pycache__/module.pyc",
        "audio/voice.wav.bak", "scratch.tmp", "notes.md~", ".DS_Store",
        "nested/.coverage", "research-os-1.0.0.zip", "research-os-1.0.0.zip.sha256",
        "release-receipt.json", "nested/generated/derived.txt",
    }
    write(repository, "nested/.gitignore", "generated/\n")
    for name in excluded:
        write(repository, name)
    write(repository, "assets/voice.wav")
    write(repository, " leading space.txt")
    commit(repository)
    write(repository, "untracked.txt")
    write(repository, ".env", "untracked secret fixture")

    inventory = names(repository)
    assert excluded.isdisjoint(inventory)
    assert {"README.md", "skills/catalog.yaml", "assets/voice.wav", " leading space.txt"} <= inventory
    assert "untracked.txt" not in inventory
    assert ".env" not in inventory


def test_machine_specific_git_ignores_do_not_change_inventory(repository: Path, tmp_path: Path) -> None:
    excludes = write(tmp_path, "global-ignore", "README.md\n")
    git(repository, "config", "core.excludesFile", str(excludes))
    write(repository, ".git/info/exclude", "skills/catalog.yaml\n")
    assert {"README.md", "skills/catalog.yaml"} <= names(repository)


@pytest.mark.parametrize("target", ["README.md", "../outside.txt", "missing.txt"])
def test_tracked_symlinks_fail_even_when_target_is_safe_or_missing(
    repository: Path, tmp_path: Path, target: str,
) -> None:
    write(tmp_path, "outside.txt", "outside fixture")
    (repository / "alias.txt").symlink_to(target)
    commit(repository)
    with pytest.raises(RuntimeError, match="non-regular"):
        packaging.source_files()


@pytest.mark.parametrize("replacement", ["file-symlink", "directory-symlink", "missing", "fifo"])
def test_replaced_worktree_paths_fail_closed(
    repository: Path, tmp_path: Path, replacement: str,
) -> None:
    source = write(repository, "nested/source.txt")
    commit(repository)
    source.unlink()
    if replacement == "file-symlink":
        source.symlink_to(write(tmp_path, "outside.txt", "outside fixture"))
    elif replacement == "directory-symlink":
        source.parent.rmdir()
        outside = tmp_path / "outside"
        write(outside, "source.txt", "outside fixture")
        source.parent.symlink_to(outside, target_is_directory=True)
    elif replacement == "fifo":
        os.mkfifo(source)
    with pytest.raises(RuntimeError, match="source"):
        packaging.source_files()


@pytest.mark.parametrize("parent_symlink", [False, True])
def test_safe_reader_rejects_symlinks_added_after_inventory(
    repository: Path, tmp_path: Path, parent_symlink: bool,
) -> None:
    source = write(repository, "nested/source.txt")
    commit(repository)
    assert source in packaging.source_files()
    source.unlink()
    outside = tmp_path / "outside"
    secret = write(outside, "source.txt", "outside-private-fixture")
    if parent_symlink:
        source.parent.rmdir()
        source.parent.symlink_to(outside, target_is_directory=True)
    else:
        source.symlink_to(secret)
    with pytest.raises(RuntimeError, match="cannot safely read") as exc:
        packaging.read_source_file(source)
    assert "outside-private-fixture" not in str(exc.value)


def test_safe_reader_rejects_fifo_without_blocking(repository: Path) -> None:
    source = repository / "README.md"
    source.unlink()
    os.mkfifo(source)
    with pytest.raises(RuntimeError, match="non-regular"):
        packaging.read_source_file(source)


@pytest.mark.parametrize(
    "name", ["bad\nname.txt", "bad\tname.txt", "back\\slash.txt", "C:drive.txt", "MANIFEST.sha256"],
)
def test_unportable_or_reserved_tracked_names_are_rejected(repository: Path, name: str) -> None:
    write(repository, name)
    commit(repository)
    with pytest.raises(RuntimeError, match="unsafe or reserved"):
        packaging.source_files()


def prepare_main(
    monkeypatch: pytest.MonkeyPatch, output: Path, *, allow_dirty: bool = False,
) -> None:
    monkeypatch.setattr(packaging, "run_release_gates", lambda: None)
    monkeypatch.setattr(
        packaging, "parse_args", lambda: argparse.Namespace(output_dir=output, allow_dirty=allow_dirty)
    )


def test_clean_release_is_reproducible_and_manifest_matches_bytes(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
) -> None:
    executable = write(repository, "scripts/example.sh", "#!/bin/sh\nexit 0\n")
    executable.chmod(0o755)
    commit(repository)
    output = tmp_path / "release"
    prepare_main(monkeypatch, output)
    assert packaging.main() == 0
    first = json.loads(capsys.readouterr().out)
    archive = Path(first["archive"])
    original = archive.read_bytes()
    original_receipt = (output / "release-receipt.json").read_bytes()
    for path in packaging.source_files():
        os.utime(path, (1_700_000_000, 1_700_000_000))
    assert packaging.main() == 0
    second = json.loads(capsys.readouterr().out)
    assert archive.read_bytes() == original
    assert (output / "release-receipt.json").read_bytes() == original_receipt
    assert first == second
    assert first["source_dirty"] is False
    assert first["source_commit"] == git(repository, "rev-parse", "HEAD")
    assert first["source_tree_sha256"] == packaging.source_tree_hash(packaging.source_files())
    assert first["archive_sha256"] == hashlib.sha256(original).hexdigest()
    assert archive.with_suffix(".zip.sha256").read_text() == f'{first["archive_sha256"]}  {archive.name}\n'
    with zipfile.ZipFile(archive) as bundle:
        prefix = "research-os-2.0.0"
        manifest = bundle.read(f"{prefix}/MANIFEST.sha256").decode()
        for line in manifest.splitlines():
            digest, name = line.split("  ", 1)
            assert digest == hashlib.sha256(bundle.read(f"{prefix}/{name}")).hexdigest()
        assert bundle.getinfo(f"{prefix}/scripts/example.sh").external_attr >> 16 == 0o755


def test_dirty_source_requires_opt_in_and_is_receipted(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
) -> None:
    write(repository, "README.md", "changed source\n")
    output = tmp_path / "release"
    prepare_main(monkeypatch, output)
    assert packaging.main() == 2
    assert "dirty source tree" in capsys.readouterr().err
    assert not output.exists()
    prepare_main(monkeypatch, output, allow_dirty=True)
    assert packaging.main() == 0
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["source_dirty"] is True
    assert receipt["dirty_status_sha256"]
    with zipfile.ZipFile(receipt["archive"]) as bundle:
        assert bundle.read("research-os-2.0.0/README.md") == b"changed source\n"


def test_failure_does_not_replace_previous_archive_or_leave_temp_files(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "release"
    existing = write(output, "research-os-2.0.0.zip", "previous release")
    prepare_main(monkeypatch, output)

    def fail_read(path: Path) -> tuple[bytes, int]:
        if path.name == "catalog.yaml":
            return b'version: "2.0.0"\n', 0o644
        raise RuntimeError("source changed during release")

    monkeypatch.setattr(packaging, "read_source_file", fail_read)
    with pytest.raises(RuntimeError, match="source changed"):
        packaging.main()
    assert existing.read_text() == "previous release"
    assert list(output.iterdir()) == [existing]


def test_clean_release_rejects_source_changes_during_build(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "release"
    prepare_main(monkeypatch, output)
    original_verify = packaging.verify_archive

    def change_after_verify(*args: object) -> dict[str, object]:
        result = original_verify(*args)
        write(repository, "README.md", "modified while packaging\n")
        return result

    monkeypatch.setattr(packaging, "verify_archive", change_after_verify)
    with pytest.raises(RuntimeError, match="source tree changed"):
        packaging.main()
    assert list(output.iterdir()) == []


def test_output_inside_repository_does_not_look_like_a_source_change(
    repository: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
) -> None:
    prepare_main(monkeypatch, repository / "custom-output")
    assert packaging.main() == 0
    assert json.loads(capsys.readouterr().out)["source_dirty"] is False


def test_dirty_content_changes_are_detected_even_when_git_status_is_unchanged(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    write(repository, "README.md", "first dirty version\n")
    output = tmp_path / "release"
    prepare_main(monkeypatch, output, allow_dirty=True)
    original_verify = packaging.verify_archive

    def change_after_verify(*args: object) -> dict[str, object]:
        result = original_verify(*args)
        write(repository, "README.md", "second dirty version\n")
        return result

    monkeypatch.setattr(packaging, "verify_archive", change_after_verify)
    with pytest.raises(RuntimeError, match="source tree changed"):
        packaging.main()
    assert list(output.iterdir()) == []


def test_release_temporary_files_do_not_follow_predictable_symlinks(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "release"
    output.mkdir()
    outside = write(tmp_path, "outside.txt", "keep outside content")
    legacy_names = [
        f".research-os-2.0.0.{os.getpid()}.tmp",
        f".research-os-2.0.0.zip.sha256.{os.getpid()}.tmp",
        f".release-receipt.{os.getpid()}.tmp",
    ]
    for name in legacy_names:
        (output / name).symlink_to(outside)
    prepare_main(monkeypatch, output)
    assert packaging.main() == 0
    assert outside.read_text() == "keep outside content"
    assert all((output / name).is_symlink() for name in legacy_names)


def test_tracked_gitlinks_are_not_silently_omitted(repository: Path) -> None:
    git(repository, "update-index", "--add", "--cacheinfo", "160000", git(repository, "rev-parse", "HEAD"), "vendor")
    with pytest.raises(RuntimeError, match="non-regular or unmerged"):
        packaging.source_files()


def test_unmerged_index_is_not_packaged(repository: Path) -> None:
    git(repository, "checkout", "--quiet", "-b", "other")
    write(repository, "README.md", "other branch\n")
    commit(repository)
    git(repository, "checkout", "--quiet", "-b", "divergent", "HEAD~1")
    write(repository, "README.md", "divergent branch\n")
    commit(repository)
    with pytest.raises(subprocess.CalledProcessError):
        git(repository, "merge", "other")
    with pytest.raises(RuntimeError, match="non-regular or unmerged"):
        packaging.source_files()


def test_archive_verification_rejects_duplicate_members(tmp_path: Path) -> None:
    archive = tmp_path / "duplicate.zip"
    data = b"fixture"
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr("release/README.md", data)
        with pytest.warns(UserWarning, match="Duplicate name"):
            bundle.writestr("release/README.md", data)
        bundle.writestr("release/MANIFEST.sha256", f"{hashlib.sha256(data).hexdigest()}  README.md\n")
    with pytest.raises(RuntimeError, match="member inventory"):
        packaging.verify_archive(archive, "release", ["README.md"])


@pytest.mark.parametrize("version", ['"../../elsewhere"', '"a/b"', "2", "null"])
def test_unsafe_version_cannot_control_output_paths(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, version: str,
) -> None:
    write(repository, "skills/catalog.yaml", f"version: {version}\n")
    commit(repository)
    output = tmp_path / "release"
    prepare_main(monkeypatch, output)
    with pytest.raises(RuntimeError, match="safe release filename"):
        packaging.main()
    assert not output.exists()
