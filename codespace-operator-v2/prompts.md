# Codespace Operator Prompts

Compact prompts for mobile/web repo work.

## Decide mode

```text
Use Codespace Operator.
repo: OWNER/REPO
goal: <goal>
task_type: inspect | debug | implement | review | preview | reproduce
runtime_need: none | build | tests | app_preview | background_process
```

## Browser Codespace

```text
Use Codespace Operator.
repo: OWNER/REPO
goal: run app from phone
runtime_need: app_preview
ports: [3000]
```

## Codespaces readiness audit

```text
Use Codespace Operator.
repo: OWNER/REPO
goal: verify repo is codespaces-ready
runtime_need: build
```

## Continue from mobile

```text
Use Codespace Operator.
repo: OWNER/REPO
goal: continue existing work from mobile
runtime_need: tests
```

## Choose the lightest surface

```text
Use Codespace Operator.
repo: OWNER/REPO
goal: choose the lightest viable workspace mode
runtime_need: none
```

## Prepare repo for Codespaces

```text
Use Codespace Operator.
repo: OWNER/REPO
goal: harden repo for Codespaces
runtime_need: build
```

## Response contract

```text
Workspace Mode
Why This Mode
Preconditions
Dry Run
Execute
Validate
Proof
Risks / Unverified Edges
```

Keep responses terse and execution-oriented.
