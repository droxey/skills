# Codespace Operator Prompts

Use these prompts to invoke the skill.

---

## Decide workspace mode

```
Use Codespace Operator.
repo: OWNER/REPO
goal: <short goal>
task_type: inspect | debug | implement | review | preview | reproduce
runtime_need: none | build | tests | app_preview | background_process
```

---

## Start browser Codespace workflow

```
Use Codespace Operator.
repo: OWNER/REPO
goal: run project locally and preview app
runtime_need: app_preview
ports: [3000]
```

---

## Diagnose repo Codespaces readiness

```
Use Codespace Operator.
repo: OWNER/REPO
goal: check whether repo is codespaces-ready
runtime_need: build
```

---

## Continue session from phone

```
Use Codespace Operator.
repo: OWNER/REPO
goal: continue work from mobile
runtime_need: tests
```

---

## Force minimal surface selection

```
Use Codespace Operator.
repo: OWNER/REPO
goal: choose lightest workspace mode
runtime_need: none
```

---

## Repo hardening request

```
Use Codespace Operator.
repo: OWNER/REPO
goal: prepare repo for codespaces
runtime_need: build
```

---

## Expected response contract

Skill must return:

```
Workspace Mode
Why This Mode
Preconditions
Dry Run
Execute
Validate
Proof
Risks / Unverified Edges
```

Responses must stay terse and execution-oriented.
