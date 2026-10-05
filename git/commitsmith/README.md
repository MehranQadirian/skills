# Commitsmith

A [Claude skill](../../README.md) that writes clean, scoped, one-line git commit messages from your diff.

```
fix(order): correct tax calculation for international shipments
perf(inventory): reduce database query time for stock lookup
refactor(user): extract password hashing logic into separate utility
test(notification): add integration tests for email delivery service
chore(deploy): update Kubernetes config for staging environment
feat(cart): apply discount code before final price calculation
fix(gateway): handle timeout errors gracefully on checkout route
```

## Format

```
type(scope): description
```

- **type**: `feat` `fix` `perf` `refactor` `test` `chore` (plus `docs` `build` `ci` `revert`)
- **scope**: one lowercase domain word, like `cart` or `gateway`
- **description**: imperative, lowercase, specific, no period, 72 characters max

## What it does

- Reads your staged diff and picks the right type and scope
- Reuses scope names already found in your git history
- Reviews or rewrites existing messages to match the style
- Flags commits that mix unrelated changes
- Commits only when you ask, never pushes on its own

## Try it

> Write a commit message for my staged changes.

> Rewrite these commit messages to match our style.

## Install

**Claude.ai:** zip this folder, then go to Settings > Capabilities > Skills > Upload.

**Claude Code:**

```bash
cp -r git/commitsmith ~/.claude/skills/
```

## Structure

```
commitsmith/
├── SKILL.md                   skill instructions for Claude
└── references/examples.md     good and bad examples
```
