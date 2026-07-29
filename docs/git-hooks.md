# Git Hooks Setup — Husky + lint-staged

DevLink uses [Husky](https://typicode.github.io/husky/) and [lint-staged](https://github.com/lint-staged/lint-staged) to enforce code quality checks before every commit and push.

---

## What runs on every commit

Husky triggers `lint-staged` via the `.husky/pre-commit` hook.  
`lint-staged` runs only on staged files, keeping the feedback loop fast.

| File pattern | Command |
| :--- | :--- |
| `src/**/*.{ts,tsx}` | `eslint --fix --max-warnings=0` + `prettier --write` |
| `src/**/*.{js,jsx,json,css,md}` | `prettier --write` |

## What runs on every push

The `.husky/pre-push` hook runs a full TypeScript type-check:

```bash
npx tsc --noEmit
```

This blocks pushes that contain type errors, even if ESLint passes.

---

## Local Setup

Hooks are installed automatically when you run `npm install` from the repo root (via the `prepare` script in the root `package.json`).

```bash
# From repo root
npm install
```

If the hooks aren't running, ensure Husky is initialized:

```bash
npx husky
```

---

## Bypassing (for emergencies only)

```bash
# Skip pre-commit
git commit --no-verify -m "your message"

# Skip pre-push
git push --no-verify
```

> ⚠️ Only bypass hooks when absolutely necessary. CI will still enforce all checks.

---

## Configuration Files

| File | Purpose |
| :--- | :--- |
| `.husky/pre-commit` | Runs lint-staged on staged files |
| `.husky/pre-push` | Runs TypeScript typecheck |
| `frontend/package.json` → `lint-staged` | Defines commands per file pattern |
| `frontend/eslint.config.js` | ESLint rules |
| `frontend/.prettierrc` | Prettier formatting rules |
