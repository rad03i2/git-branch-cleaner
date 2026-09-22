# Git Branch Cleaner

A small, dependency-free Python CLI for finding **merged local Git branches** that are safe candidates for cleanup. Preview is the default; deletion is explicit and guarded.

> Author: **Radwan Abdulhadi Ahmed** · **رضوان عبدالهادي أحمد** · GitHub: **@rad03i2**

## English

### Overview
Long-lived repositories accumulate local branches that have already been merged. Removing them manually is repetitive, while aggressive cleanup scripts can delete the wrong branch. Git Branch Cleaner focuses on a narrow, auditable workflow: identify merged branches, exclude protected/current branches, optionally apply an age threshold, preview the exact candidates, then delete only after explicit confirmation.

### Key features
- Scans **local branches only**; it never contacts or modifies remotes.
- Determines merge status relative to an explicit or automatically selected base branch.
- Protects `main`, `master`, `develop`, `development`, `dev`, `trunk`, `production`, `release`, the selected base, and any names supplied with `--protect`.
- Never selects the currently checked-out branch.
- Optional `--min-age DAYS` filter based on the branch tip's commit date.
- Safe preview by default; destructive mode requires both `--delete` and `--yes`.
- Uses `git branch -d`, not force deletion, so Git performs an additional merged-branch safety check.
- Human-readable and JSON output.
- Reusable Python API and no runtime Python dependencies.

### Requirements
- Python 3.10+
- Git available on `PATH`
- A local Git repository

### Installation
From a clone:

```bash
git clone https://github.com/rad03i2/git-branch-cleaner.git
cd git-branch-cleaner
python -m pip install .
```

For development:

```bash
python -m pip install -e . pytest
```

### Usage
Preview merged branches relative to the repository's usual base branch:

```bash
git-branch-cleaner /path/to/repo
```

Only show candidates whose tip commit is at least 14 days old:

```bash
git-branch-cleaner . --base main --min-age 14
```

Add project-specific protected branches:

```bash
git-branch-cleaner . --protect staging --protect qa
```

Machine-readable preview:

```bash
git-branch-cleaner . --base main --json
```

After reviewing the preview, delete the same eligible local branches:

```bash
git-branch-cleaner . --base main --min-age 14 --delete --yes
```

You can also run `python -m git_branch_cleaner` after installation.

### Python API
```python
from git_branch_cleaner import scan_branches, cleanup_candidates

base, branches = scan_branches(".", base="main", protected=["staging"])
candidates = cleanup_candidates(branches, min_age_days=14)
for branch in candidates:
    print(branch.name, branch.age_days)
```

### Preview guidance
This is a terminal application, so screenshots are optional. For documentation or release previews, capture the default preview output showing the base branch and candidate list. Do not publish terminal captures containing private repository paths or branch names unless intended.

### Configuration
There is intentionally no configuration file and no environment-variable requirement. Use CLI flags so every cleanup decision is visible in shell history and CI scripts. `--protect` is repeatable.

### Project structure
```text
src/git_branch_cleaner/
  __init__.py     Public API and version
  __main__.py     python -m entry point
  cli.py          CLI parsing, output and confirmation guard
  core.py         Git inspection, candidate rules and deletion
tests/
  test_core.py        Selection/safety unit tests
  test_integration.py Real temporary Git repository integration test
.github/workflows/ci.yml
```

### Testing
```bash
python -m pip install -e . pytest
pytest
python -m compileall -q src tests
```

CI runs these checks on Ubuntu, Windows and macOS with supported Python versions. Integration tests create only temporary local repositories.

### Security and privacy
The tool invokes the local `git` executable with argument arrays rather than a shell. It does not use network APIs, telemetry, credentials, tokens, remote deletion, `git push`, or force deletion. Branch names are passed after `--` to the delete command. Always inspect the preview before destructive mode and keep important work committed/pushed according to your own backup policy.

See [SECURITY.md](SECURITY.md) for reporting security issues.

### Limitations
- Cleans local branches only; remote branch deletion is deliberately unsupported.
- Merge status follows Git's commit-ancestry semantics relative to the selected base; squash-merged or rebased branches may not appear as merged.
- Age means the age of the branch tip commit, not branch creation time (Git does not normally store branch creation time).
- Worktrees and unusual Git workflows can impose additional Git-side restrictions; `git branch -d` remains the final safety authority.
- The tool does not infer whether a branch name is business-critical beyond its protection rules.

### Optional roadmap
Future work may add an opt-in interactive selector, worktree-aware explanations, and configurable protection patterns. Remote deletion is intentionally not on the default roadmap.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Please include tests for behavior changes and preserve preview-first safety.

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
تتراكم في المستودعات فروع محلية انتهى العمل عليها وتم دمجها، ويصبح تنظيفها يدويًا متكررًا، بينما قد تكون سكربتات الحذف العدوانية خطرة. يركز Git Branch Cleaner على مسار واضح وقابل للمراجعة: اكتشاف الفروع المدمجة، استبعاد الفروع المحمية والفرع الحالي، تطبيق حد للعمر عند الحاجة، عرض ما سيُحذف أولًا، ثم السماح بالحذف فقط بعد تأكيد صريح.

### أهم الميزات
- يفحص **الفروع المحلية فقط** ولا يتصل بالمستودع البعيد ولا يعدله.
- يحدد حالة الدمج نسبةً إلى فرع أساس تختاره أو يكتشفه البرنامج.
- يحمي تلقائيًا `main` و`master` و`develop` و`development` و`dev` و`trunk` و`production` و`release` وفرع الأساس، ويمكن إضافة فروع أخرى عبر `--protect`.
- لا يختار الفرع المفتوح حاليًا للحذف.
- يدعم `--min-age DAYS` لاعتماد عمر آخر commit في الفرع.
- وضع المعاينة هو الافتراضي، والحذف يتطلب `--delete --yes` معًا.
- يستخدم `git branch -d` بدل الحذف الإجباري، لذلك يجري Git فحص أمان إضافيًا.
- مخرجات نصية واضحة أو JSON للأتمتة.
- Python API قابلة لإعادة الاستخدام، ومن دون اعتماديات تشغيل خارجية لبايثون.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث وGit ضمن `PATH` ومستودع Git محليًا.

```bash
git clone https://github.com/rad03i2/git-branch-cleaner.git
cd git-branch-cleaner
python -m pip install .
```

للتطوير والاختبار:

```bash
python -m pip install -e . pytest
pytest
```

### الاستخدام
معاينة الفروع المدمجة:

```bash
git-branch-cleaner . --base main
```

اختيار الفروع التي مضى على آخر commit فيها 14 يومًا على الأقل مع حماية فرع إضافي:

```bash
git-branch-cleaner . --base main --min-age 14 --protect staging
```

إخراج JSON:

```bash
git-branch-cleaner . --base main --json
```

بعد مراجعة النتيجة فقط، نفّذ الحذف:

```bash
git-branch-cleaner . --base main --min-age 14 --delete --yes
```

يمكن أيضًا تشغيل `python -m git_branch_cleaner` بعد التثبيت.

### Python API
```python
from git_branch_cleaner import scan_branches, cleanup_candidates

base, branches = scan_branches(".", base="main", protected=["staging"])
candidates = cleanup_candidates(branches, min_age_days=14)
```

### المعاينة والإعداد
المشروع أداة طرفية، لذلك لا يحتاج إلى واجهة رسومية. عند إعداد صورة للمشروع يمكن تصوير خرج المعاينة بعد إخفاء المسارات أو أسماء الفروع الخاصة. لا يوجد ملف إعداد أو متغيرات بيئة مطلوبة؛ جميع القرارات المهمة ظاهرة كخيارات CLI، ويمكن تكرار `--protect`.

### بنية المشروع والاختبارات
الكود الأساسي موجود في `src/git_branch_cleaner/`، والاختبارات في `tests/`، وCI في `.github/workflows/ci.yml`. تشمل الاختبارات قواعد اختيار الفروع واختبار تكامل ينشئ مستودع Git مؤقتًا ويدمج فرعًا ثم يتحقق من تنظيفه بأمان.

```bash
pytest
python -m compileall -q src tests
```

### الأمان والخصوصية
لا تستخدم الأداة الشبكة أو telemetry أو مفاتيح API أو بيانات اعتماد، ولا تنفذ `git push` ولا حذفًا بعيدًا ولا حذفًا إجباريًا. تستدعي Git بقائمة arguments من دون shell. يوصى دائمًا بمراجعة المعاينة قبل الحذف والاحتفاظ بنسخة مناسبة من العمل المهم. راجع [SECURITY.md](SECURITY.md).

### القيود
- التنظيف للفروع المحلية فقط.
- الفروع التي تم squash-merge أو rebase لها قد لا يعتبرها Git مدمجة حسب ancestry.
- العمر هو عمر آخر commit وليس تاريخ إنشاء الفرع لأن Git لا يخزن هذا التاريخ عادةً.
- قد تمنع worktrees أو إعدادات Git خاصة حذف بعض الفروع؛ يبقى `git branch -d` حكم الأمان النهائي.
- لا يمكن للأداة معرفة الأهمية التجارية للفرع إلا من قواعد الحماية المحددة.

### التطوير الاختياري
يمكن مستقبلًا إضافة اختيار تفاعلي اختياري، وشرح أوضح لحالات worktree، وأنماط حماية قابلة للتخصيص. حذف الفروع البعيدة غير مستهدف افتراضيًا حفاظًا على الأمان.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) قبل إرسال تغييرات، وأضف اختبارات للسلوك الجديد. المشروع مرخص وفق MIT؛ راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
