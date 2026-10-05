---
name: commitsmith
description: Writes git commit messages in a strict, scoped one-line style such as "fix(order): correct tax calculation for international shipments". Use whenever the user asks for a commit message, wants to commit changes, or asks to review, rewrite or squash commit messages, even if they only say "commit this" or "write a commit". Reads the staged diff to pick the right type, scope and wording.
---

# commitsmith

One consistent commit style: `type(scope): description`

```
fix(order): correct tax calculation for international shipments
perf(inventory): reduce database query time for stock lookup
refactor(user): extract password hashing logic into separate utility
test(notification): add integration tests for email delivery service
chore(deploy): update Kubernetes config for staging environment
feat(cart): apply discount code before final price calculation
fix(gateway): handle timeout errors gracefully on checkout route
```

## Workflow

1. **Read the change.** Run `git diff --staged` (if empty, `git diff`). Also run `git status --short` to see which files are involved.
2. **Pick the type** from the table below.
3. **Pick the scope**: the one domain area the change belongs to.
4. **Write the description**: what the change does, in the imperative mood.
5. **Check the rules** below, then output the message in a code block.
6. If the user asked to commit, run `git commit -m "<message>"`. Never push unless asked.

## Types

| Type | Use for |
|---|---|
| `feat` | New behavior or capability for users |
| `fix` | Bug fix |
| `perf` | Performance improvement with no behavior change |
| `refactor` | Code restructure with no behavior change |
| `test` | Adding or updating tests only |
| `chore` | Config, tooling, dependencies, deployment, maintenance |
| `docs` | Documentation only |
| `build` | Build system or packaging |
| `ci` | CI pipeline changes |
| `revert` | Reverting an earlier commit |

If two types fit, choose the one that describes the main intent. A bug fix that also adds a test is `fix`.

## Scope

- Required. One lowercase word naming the domain: `order`, `inventory`, `user`, `notification`, `deploy`, `cart`, `gateway`.
- Prefer the business area over a file or folder name (`cart`, not `cart-service.ts`).
- Use the singular form and no spaces. Join two words with a hyphen only when unavoidable (`user-profile`).
- Follow the scope names already used in `git log --oneline -20` when they exist.
- If a change spans several areas, use the area where the main behavior changes. If it truly has no single owner, split it into separate commits.

## Description rules

- Imperative mood, lowercase first letter: `add`, `fix`, `handle`, `reduce`, `extract`, `update`, `apply`, `correct`.
- Be specific: say what and where, not "update stuff" or "fix bug".
- No period at the end.
- Whole first line at most 72 characters.
- No ticket numbers, emojis, author names or file names in the first line.
- Describe the change itself, not the process ("fix typo" is fine, "address review comments" is not).

## Body (optional)

Add a body only when the reason is not obvious from the diff. Leave one blank line after the first line, wrap at 72 characters, and explain **why**, not what. Breaking changes go in a final `BREAKING CHANGE:` line.

## Reviewing or rewriting messages

When given existing messages, show each one as `before -> after` and keep only the changes that fix a rule. If a commit mixes unrelated changes, say so and suggest how to split it.

## Do not

- Do not write multiple lines for a simple change.
- Do not invent a scope that is not in the project when a matching one already exists.
- Do not use past tense (`fixed`) or gerunds (`fixing`).
- Do not commit or push without the user asking for it.

See `references/examples.md` for more good and bad examples.
