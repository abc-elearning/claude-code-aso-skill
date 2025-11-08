## Change Type
<!-- Select one by placing an 'x' in the brackets -->
- [ ] Bug Fix
- [ ] Feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Security
- [ ] Performance
- [ ] Workflow/CI

## Description
<!-- 1-2 sentences: Why this change (not what changed) -->



## ASO Impact
<!-- Which modules/functionality affected? -->
**Affected Modules:**
- [ ] keyword_analyzer.py
- [ ] metadata_optimizer.py
- [ ] competitor_analyzer.py
- [ ] aso_scorer.py
- [ ] ab_test_planner.py
- [ ] localization_helper.py
- [ ] review_analyzer.py
- [ ] launch_checklist.py
- [ ] ASO agents
- [ ] GitHub workflows
- [ ] Documentation only
- [ ] Other: _________

**Platform Impact:**
- [ ] Apple App Store
- [ ] Google Play Store
- [ ] Both platforms
- [ ] Not platform-specific

## Testing
<!-- Manual testing performed -->
**Testing Checklist:**
- [ ] Tested with Python 3.8+
- [ ] All functions execute without errors
- [ ] Character limit validation working (if applicable)
- [ ] No external dependencies added
- [ ] Platform-specific logic correct (if applicable)

**Test Commands Run:**
```bash
# Example:
python -m py_compile app-store-optimization/keyword_analyzer.py
# or
python app-store-optimization/metadata_optimizer.py
```

## Character Limits Validated
<!-- For metadata changes only -->
- [ ] Apple App Store limits validated (Title: 30, Subtitle: 30, Keywords: 100)
- [ ] Google Play Store limits validated (Title: 50, Short Desc: 80)
- [ ] N/A - No metadata changes

## Pre-merge Checklist
**Code Quality:**
- [ ] Code follows Python best practices (PEP 8)
- [ ] Docstrings added/updated for public functions
- [ ] No console.log, print(), or debug statements
- [ ] No hardcoded credentials or API keys
- [ ] Error handling implemented for edge cases

**Documentation:**
- [ ] CHANGELOG.md updated (if user-facing change)
- [ ] README.md updated (if installation/usage changed)
- [ ] Inline comments added for complex ASO logic
- [ ] Wiki will be auto-updated (documentation changes only)

**Quality Gates:**
- [ ] Ruff linting passes locally (`ruff check app-store-optimization/`)
- [ ] Python syntax valid (`python -m py_compile ...`)
- [ ] GitHub Actions quality checks will pass

## Linked Issues
<!-- Link related issues using #number -->
Closes #

## Additional Context
<!-- Any other context, screenshots, or notes -->


---
**For Reviewers:**
- [ ] ASO logic correctness verified
- [ ] Character limits validated
- [ ] No security vulnerabilities
- [ ] Documentation sufficient
