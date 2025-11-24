# ⚡ Reusable Workflows - Quick Reference

## 🎯 What Are They?

**Reusable workflows** = Workflows that can be called from other workflows (like functions/templates)

**Key Benefit**: Write once, use many times - eliminates code duplication!

---

## 📝 Basic Structure

### Reusable Workflow (Template)

```yaml
name: Reusable Workflow Name

on:
  workflow_call:  # ⚠️ Only trigger allowed!
    inputs:
      input-name:
        description: 'Description'
        required: true
        type: string
    outputs:
      output-name:
        description: 'Output description'
        value: ${{ jobs.job-name.outputs.status }}

jobs:
  job-name:
    runs-on: ubuntu-latest
    outputs:
      status: ${{ steps.step-name.outputs.status }}
    steps:
      - name: Use input
        run: echo "${{ inputs.input-name }}"
```

### Calling Workflow (User)

```yaml
name: Main Workflow

on:
  push:
    branches: [main]

jobs:
  call-reusable:
    uses: ./.github/workflows/reusable/workflow-name.yml
    with:
      input-name: 'value'
  
  use-output:
    needs: call-reusable
    runs-on: ubuntu-latest
    steps:
      - name: Get output
        run: echo "${{ needs.call-reusable.outputs.output-name }}"
```

---

## 🔑 Key Syntax

### Access Inputs (in reusable workflow)
```yaml
${{ inputs.input-name }}
```

### Access Outputs (in calling workflow)
```yaml
${{ needs.job-id.outputs.output-name }}
```

### Reference Reusable Workflow
```yaml
# Same repository
uses: ./.github/workflows/reusable/workflow.yml

# Different repository
uses: owner/repo/.github/workflows/workflow.yml@branch
```

---

## 📋 Input Types

| Type | Example | Use Case |
|------|----------|----------|
| `string` | `version: '3.11'` | Text values |
| `number` | `timeout: 60` | Numeric values |
| `boolean` | `verbose: true` | True/false flags |
| `choice` | `env: [dev, prod]` | Select from options |
| `environment` | `env: production` | Environment name |

---

## ✅ Input Definition Template

```yaml
on:
  workflow_call:
    inputs:
      input-name:
        description: 'What this input does'
        required: true          # or false
        type: string            # string, number, boolean, choice, environment
        default: 'default'     # Optional default value
```

---

## 📤 Output Definition Template

```yaml
on:
  workflow_call:
    outputs:
      output-name:
        description: 'What this output represents'
        value: ${{ jobs.job-name.outputs.status }}
        # ⚠️ Must reference JOB outputs, not step outputs directly!
```

---

## 🔐 Secrets

### In Reusable Workflow
```yaml
on:
  workflow_call:
    secrets:
      API_KEY:
        required: true
      TOKEN:
        required: false
```

### In Calling Workflow
```yaml
jobs:
  deploy:
    uses: ./.github/workflows/reusable/deploy.yml
    secrets:
      API_KEY: ${{ secrets.API_KEY }}  # Must explicitly pass!
```

---

## ⚠️ Important Rules

1. **Only `workflow_call` trigger** - No `push`, `pull_request`, etc.
2. **Outputs reference jobs** - `${{ jobs.job.outputs.x }}` not `${{ steps.step.outputs.x }}`
3. **Secrets must be passed** - Explicitly pass from calling workflow
4. **Path starts with `./`** - `./.github/workflows/...` not `.github/workflows/...`

---

## 🎯 Common Patterns

### Conditional Setup Based on Input
```yaml
- name: Set up Python
  if: inputs.language == 'python'
  uses: actions/setup-python@v5
  with:
    python-version: ${{ inputs.version }}

- name: Set up Node.js
  if: inputs.language == 'node'
  uses: actions/setup-node@v4
  with:
    node-version: ${{ inputs.version }}
```

### Setting Job Outputs
```yaml
jobs:
  test:
    outputs:
      status: ${{ steps.test-result.outputs.status }}
    steps:
      - name: Run tests
        id: test-result
        run: |
          pytest
          echo "status=success" >> $GITHUB_OUTPUT
```

### Using Outputs in Calling Workflow
```yaml
jobs:
  test:
    uses: ./.github/workflows/reusable/test.yml
  
  deploy:
    needs: test
    if: needs.test.outputs.status == 'success'
    uses: ./.github/workflows/reusable/deploy.yml
```

---

## ❌ Common Mistakes

| Mistake | Fix |
|---------|-----|
| `on: push:` + `workflow_call:` | Only `workflow_call:` |
| `value: ${{ steps.x.outputs.y }}` | `value: ${{ jobs.x.outputs.y }}` |
| Missing `secrets:` block | Add `secrets:` and pass explicitly |
| `uses: .github/...` | `uses: ./.github/...` (needs `./`) |

---

## 📊 Comparison

| Feature | Regular Workflow | Reusable Workflow |
|---------|-----------------|-------------------|
| Triggers | `push`, `pr`, etc. | Only `workflow_call` |
| Can be called | ❌ No | ✅ Yes |
| Inputs | ❌ No | ✅ Yes |
| Outputs | ❌ No | ✅ Yes |
| Use case | Standalone | Shared logic |

---

## 🎓 Quick Example

### Reusable: `build-and-test.yml`
```yaml
on:
  workflow_call:
    inputs:
      language:
        type: choice
        options: [python, node]
    outputs:
      status:
        value: ${{ jobs.test.outputs.status }}

jobs:
  test:
    outputs:
      status: ${{ steps.result.outputs.status }}
    steps:
      - run: echo "Testing ${{ inputs.language }}"
      - id: result
        run: echo "status=success" >> $GITHUB_OUTPUT
```

### Calling: `main.yml`
```yaml
jobs:
  test:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: python
```

---

**📚 For detailed explanations, see [`reusable-workflows-guide.md`](reusable-workflows-guide.md)**




