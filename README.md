[![](https://travis-ci.org/Lucas-C/pre-commit-hooks-safety.svg?branch=master)](https://travis-ci.org/Lucas-C/pre-commit-hooks-safety)

A [pre-commit](http://pre-commit.com) hook to check your Python dependencies against [safety-db](//github.com/pyupio/safety-db).

It checks all files containing `requirements` in their name in the repo.

It also installs each `requirements` file (and subsequently uninstalls) and runs safety on the resulting environment.  This forces all unpinned packages in requirements files to a fixed version.

## Usage
```
-   repo: https://github.com/jsumnerPhD/pre-commit-hooks-safety
    sha: v1.1.3
    hooks:
    -   id: python-safety-dependencies-check-all
```

## Alternative local hook
You'll need to `pip install safety` beforehand:
```
-   repo: local
    hooks:
    -   id: python-safety-dependencies-check
        entry: safety
        args: [check, --full-report]
        language: system
        files: requirements
```
