# Contributing (Git Flow)

This repository follows **Git Flow**.

## Branches

- **`main`**: production-ready state only. Only release/hotfix merges go here.
- **`develop`**: integration branch for the next release.

## Branch naming

- **Feature**: `feature/<short-description>`
  - Base: `develop`
  - Merge target: `develop`
- **Release**: `release/<version>`
  - Base: `develop`
  - Merge targets: `main` and back to `develop`
- **Hotfix**: `hotfix/<version-or-issue>`
  - Base: `main`
  - Merge targets: `main` and back to `develop`

Examples:

- `feature/add-healthcheck`
- `release/1.0.0`
- `hotfix/1.0.1`

## Workflow

### Feature development

```bash
git checkout develop
git pull
git checkout -b feature/<name>

# work, commit
git add -A
git commit -m "feat: <message>"

git push -u origin HEAD
# open PR -> develop
```

### Release

```bash
git checkout develop
git pull
git checkout -b release/<version>

# optional: version bump, docs, final fixes
git push -u origin HEAD
# open PR -> main
```

After merging release into `main`:

```bash
git checkout main
git pull
git tag -a v<version> -m "Release v<version>"
git push --tags

# merge main back into develop
git checkout develop
git pull
git merge main
git push
```

### Hotfix

```bash
git checkout main
git pull
git checkout -b hotfix/<version-or-issue>

# fix, commit
git push -u origin HEAD
# open PR -> main
```

After merging hotfix into `main`, merge `main` back into `develop` the same way as with releases.

## Commit messages

Recommended format:

- `feat: ...`
- `fix: ...`
- `chore: ...`
- `docs: ...`

