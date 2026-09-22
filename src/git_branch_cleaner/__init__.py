"""Safe local Git branch cleanup utilities."""

__version__ = "1.0.0"

from .core import Branch, DEFAULT_PROTECTED, GitError, cleanup_candidates, delete_branches, repository_root, scan_branches

__all__ = [
    "Branch", "DEFAULT_PROTECTED", "GitError", "cleanup_candidates",
    "delete_branches", "repository_root", "scan_branches", "__version__",
]
