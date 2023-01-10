# django-debug-false-checker

[![PyPI version](https://badge.fury.io/py/django-debug-false-checker.svg)](https://badge.fury.io/py/django-debug-false-checker)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

`django-debug-false-checker` will check that you're not changing the django DEBUG's
setting by mistake.

## Installation

```yaml
- repo: https://github.com/Pierre-Sassoulas/django-debug-false-checker/
  rev: v0.0.4
  hooks:
    - id: django-debug-false-checker
```
