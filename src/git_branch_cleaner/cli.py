from __future__ import annotations

import argparse
import json
import sys

from .core import GitError, cleanup_candidates, delete_branches, scan_branches
from . import __version__

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="git-branch-cleaner",
        description="Safely find and optionally delete merged local Git branches.",
    )
    parser.add_argument("path", nargs="?", default=".", help="Repository path (default: current directory)")
    parser.add_argument("--base", help="Base branch used to determine merged branches")
    parser.add_argument("--min-age", type=int, default=0, metavar="DAYS", help="Only select branches at least DAYS old")
    parser.add_argument("--protect", action="append", default=[], metavar="BRANCH", help="Additional protected branch; repeatable")
    parser.add_argument("--delete", action="store_true", help="Delete selected branches using safe 'git branch -d'")
    parser.add_argument("--yes", action="store_true", help="Required with --delete; confirms non-interactive deletion")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__} — Radwan Abdulhadi Ahmed / @rad03i2")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.min_age < 0:
        _parser().error("--min-age must be >= 0")
    if args.delete and not args.yes:
        print("Refusing deletion without --yes. Run without --delete to preview first.", file=sys.stderr)
        return 2
    try:
        base, branches = scan_branches(args.path, base=args.base, min_age_days=args.min_age, protected=args.protect)
        candidates = cleanup_candidates(branches, args.min_age)
        deleted = delete_branches(args.path, candidates) if args.delete else []
    except (GitError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({
            "base": base,
            "candidate_count": len(candidates),
            "candidates": [b.to_dict() for b in candidates],
            "deleted": deleted,
            "dry_run": not args.delete,
        }, indent=2))
        return 0

    mode = "DELETE" if args.delete else "PREVIEW"
    print(f"Git Branch Cleaner — {mode}\nBase: {base}\n")
    if not candidates:
        print("No eligible merged branches found.")
        return 0
    for branch in candidates:
        action = "deleted" if branch.name in deleted else "would delete"
        print(f"- {branch.name:<28} {branch.age_days:>4}d  {branch.commit[:10]}  {action}")
    if not args.delete:
        print(f"\n{len(candidates)} candidate(s). Re-run with --delete --yes after reviewing the list.")
    else:
        print(f"\nDeleted {len(deleted)} branch(es).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
