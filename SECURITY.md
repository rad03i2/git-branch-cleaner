# Security Policy

## Supported version
The latest release on the default branch is supported.

## Security model
Git Branch Cleaner operates only on local Git branches. It does not require network access, credentials, tokens, remote APIs, or elevated privileges. Destructive operation is opt-in and uses `git branch -d` rather than force deletion.

Treat repository paths and branch names as potentially sensitive when sharing logs or screenshots. The tool does not intentionally transmit them anywhere.

## Reporting a vulnerability
Please report security concerns privately through GitHub's repository security reporting features when available. Do not open a public issue containing exploit details, credentials, tokens, private paths, or other sensitive information.

Include the affected version, platform, reproduction steps, expected behavior, and impact where possible.

Maintainer: **Radwan Abdulhadi Ahmed / رضوان عبدالهادي أحمد / @rad03i2**.
