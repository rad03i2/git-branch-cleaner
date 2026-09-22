from __future__ import annotations

import os
import subprocess

from git_branch_cleaner import cleanup_candidates, delete_branches, scan_branches

def git(repo, *args, env=None):
    merged_env = os.environ.copy()
    merged_env.update(env or {})
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True, capture_output=True, env=merged_env).stdout.strip()

def make_repo(tmp_path):
    git(tmp_path, "init", "-b", "main")
    git(tmp_path, "config", "user.name", "Test User")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    (tmp_path / "base.txt").write_text("base\n", encoding="utf-8")
    git(tmp_path, "add", "base.txt")
    git(tmp_path, "commit", "-m", "initial")
    git(tmp_path, "checkout", "-b", "feature/done")
    (tmp_path / "done.txt").write_text("done\n", encoding="utf-8")
    git(tmp_path, "add", "done.txt")
    git(tmp_path, "commit", "-m", "done")
    git(tmp_path, "checkout", "main")
    git(tmp_path, "merge", "--no-ff", "feature/done", "-m", "merge feature")
    git(tmp_path, "checkout", "-b", "feature/open")
    (tmp_path / "open.txt").write_text("open\n", encoding="utf-8")
    git(tmp_path, "add", "open.txt")
    git(tmp_path, "commit", "-m", "open")
    git(tmp_path, "checkout", "main")

def test_scan_and_safe_delete(tmp_path):
    make_repo(tmp_path)
    base, branches = scan_branches(tmp_path, base="main")
    assert base == "main"
    by_name = {b.name: b for b in branches}
    assert by_name["main"].protected
    assert by_name["feature/done"].merged
    assert not by_name["feature/open"].merged
    candidates = cleanup_candidates(branches)
    assert [b.name for b in candidates] == ["feature/done"]
    assert delete_branches(tmp_path, candidates) == ["feature/done"]
    assert "feature/done" not in git(tmp_path, "branch", "--format=%(refname:short)").splitlines()
    assert "feature/open" in git(tmp_path, "branch", "--format=%(refname:short)").splitlines()
