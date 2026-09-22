# Contributing

Thanks for improving Git Branch Cleaner.

1. Create a focused branch and keep changes small.
2. Use Python 3.10+ and avoid runtime dependencies unless they provide clear value.
3. Preserve the safety contract: preview by default, no remote deletion, no force deletion, and protected/current branches must never become candidates.
4. Install development tools with `python -m pip install -e . pytest`.
5. Run `pytest` and `python -m compileall -q src tests` before proposing a change.
6. Add or update tests for behavior changes. Prefer temporary repositories for Git integration tests.
7. Keep README commands synchronized with actual CLI behavior.

Please do not include secrets, personal repository data, generated environments, or unrelated files in contributions.

## المؤلف
Maintained by **Radwan Abdulhadi Ahmed / رضوان عبدالهادي أحمد / @rad03i2**.
