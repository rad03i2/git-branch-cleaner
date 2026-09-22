from datetime import datetime, timedelta, timezone

import pytest

from git_branch_cleaner.core import Branch, GitError, cleanup_candidates, delete_branches

NOW = datetime(2026, 9, 22, tzinfo=timezone.utc)

def branch(name, *, merged=True, protected=False, current=False, age=30):
    return Branch(name, "a" * 40, NOW - timedelta(days=age), current, merged, protected, age)

def test_candidates_require_merged_unprotected_noncurrent_and_age():
    branches = [
        branch("feature/old", age=30),
        branch("feature/new", age=2),
        branch("main", protected=True),
        branch("active", current=True),
        branch("unmerged", merged=False),
    ]
    assert [b.name for b in cleanup_candidates(branches, 7)] == ["feature/old"]

def test_zero_age_allows_recent_merged_branch():
    assert [b.name for b in cleanup_candidates([branch("done", age=0)], 0)] == ["done"]

def test_delete_rejects_unmerged_before_running_git(tmp_path):
    with pytest.raises(GitError, match="Refusing unsafe deletion"):
        # Repository lookup happens first, so use a tiny initialized repository.
        import subprocess
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        delete_branches(tmp_path, [branch("work", merged=False)])
