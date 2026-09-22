from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import subprocess
from typing import Iterable

DEFAULT_PROTECTED = frozenset({"main", "master", "develop", "development", "dev", "trunk", "production", "release"})

class GitError(RuntimeError):
    """Raised when a Git command cannot be completed safely."""

@dataclass(frozen=True)
class Branch:
    name: str
    commit: str
    committed_at: datetime
    current: bool
    merged: bool
    protected: bool
    age_days: int

    def to_dict(self) -> dict:
        data = asdict(self)
        data["committed_at"] = self.committed_at.isoformat()
        return data

def _git(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=False
    )
    if check and proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip() or "Git command failed"
        raise GitError(message)
    return proc.stdout.strip()

def repository_root(path: str | Path = ".") -> Path:
    candidate = Path(path).expanduser().resolve()
    if not candidate.exists():
        raise GitError(f"Path does not exist: {candidate}")
    root = _git(candidate, "rev-parse", "--show-toplevel")
    return Path(root).resolve()

def _resolve_base(repo: Path, base: str | None) -> str:
    if base:
        _git(repo, "rev-parse", "--verify", f"refs/heads/{base}")
        return base
    for name in ("main", "master", "trunk", "develop"):
        if _git(repo, "show-ref", "--verify", "--quiet", f"refs/heads/{name}", check=False) == "":
            # show-ref --quiet has no stdout; verify separately because return code matters.
            proc = subprocess.run(["git", "-C", str(repo), "show-ref", "--verify", "--quiet", f"refs/heads/{name}"])
            if proc.returncode == 0:
                return name
    current = _git(repo, "branch", "--show-current")
    if not current:
        raise GitError("Detached HEAD: specify --base explicitly.")
    return current

def scan_branches(
    path: str | Path = ".",
    *,
    base: str | None = None,
    min_age_days: int = 0,
    protected: Iterable[str] = (),
    now: datetime | None = None,
) -> tuple[str, list[Branch]]:
    if min_age_days < 0:
        raise ValueError("min_age_days must be >= 0")
    repo = repository_root(path)
    base_name = _resolve_base(repo, base)
    protected_set = DEFAULT_PROTECTED | set(protected) | {base_name}
    merged_names = set(filter(None, _git(repo, "branch", "--merged", base_name, "--format=%(refname:short)").splitlines()))
    current_name = _git(repo, "branch", "--show-current")
    raw = _git(repo, "for-each-ref", "--format=%(refname:short)|%(objectname)|%(committerdate:iso-strict)", "refs/heads/")
    clock = now or datetime.now(timezone.utc)
    if clock.tzinfo is None:
        clock = clock.replace(tzinfo=timezone.utc)
    branches: list[Branch] = []
    for line in filter(None, raw.splitlines()):
        name, commit, timestamp = line.split("|", 2)
        committed_at = datetime.fromisoformat(timestamp).astimezone(timezone.utc)
        age = max(0, (clock.astimezone(timezone.utc) - committed_at).days)
        branches.append(Branch(
            name=name,
            commit=commit,
            committed_at=committed_at,
            current=name == current_name,
            merged=name in merged_names,
            protected=name in protected_set,
            age_days=age,
        ))
    return base_name, sorted(branches, key=lambda item: (-item.age_days, item.name))

def cleanup_candidates(branches: Iterable[Branch], min_age_days: int = 0) -> list[Branch]:
    return [b for b in branches if b.merged and not b.current and not b.protected and b.age_days >= min_age_days]

def delete_branches(path: str | Path, branches: Iterable[Branch]) -> list[str]:
    repo = repository_root(path)
    deleted: list[str] = []
    for branch in branches:
        if branch.current or branch.protected or not branch.merged:
            raise GitError(f"Refusing unsafe deletion of branch: {branch.name}")
        # -d is intentionally non-forcing: Git performs its own merged-branch safety check.
        _git(repo, "branch", "-d", "--", branch.name)
        deleted.append(branch.name)
    return deleted
