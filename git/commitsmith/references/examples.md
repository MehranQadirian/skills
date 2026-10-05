# Examples

## Good

```
feat(auth): add refresh token rotation
fix(checkout): prevent double submit on payment button
perf(search): cache category filters for repeated queries
refactor(billing): split invoice builder into smaller functions
test(payment): cover declined card flow with integration tests
chore(deps): bump express to 4.19.2
docs(api): document pagination parameters
ci(pipeline): run lint before unit tests
build(docker): reduce image size with multi-stage build
revert(cart): undo discount stacking change
```

## Bad, with fixes

| Bad | Why | Better |
|---|---|---|
| `fixed bug` | no scope, vague, past tense | `fix(order): prevent negative quantity on update` |
| `feat: Add new button.` | no scope, capitalized, period | `feat(profile): add avatar upload button` |
| `update(cart)` | invalid type, no description | `fix(cart): recalculate total after coupon removal` |
| `fix(cart-service.ts): null check` | file name as scope | `fix(cart): handle empty cart on checkout` |
| `chore(deploy): update config for staging and also fix login bug` | two changes in one | split into `chore(deploy): ...` and `fix(auth): ...` |
| `refactor(user): refactoring` | says nothing | `refactor(user): extract password hashing into utility` |

## Choosing a type quickly

| The diff... | Type |
|---|---|
| changes what the user sees or can do | `feat` |
| corrects wrong behavior | `fix` |
| makes the same behavior faster or lighter | `perf` |
| moves or rewrites code, same behavior | `refactor` |
| touches only test files | `test` |
| touches only config, deps, scripts, infra | `chore` |
