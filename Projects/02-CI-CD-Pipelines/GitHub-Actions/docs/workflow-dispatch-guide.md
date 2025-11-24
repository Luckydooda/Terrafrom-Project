# 🎛️ Workflow Dispatch with Inputs - Complete Guide

## 📋 Table of Contents
1. [What is Workflow Dispatch?](#what-is-workflow-dispatch)
2. [Why Do We Need It?](#why-do-we-need-it)
3. [How Does It Work?](#how-does-it-work)
4. [Input Types](#input-types)
5. [Task 11 Implementation Guide](#task-11-implementation-guide)

---

## 🎯 What is Workflow Dispatch?

**Workflow Dispatch** is a GitHub Actions trigger that allows you to **manually run workflows** from the GitHub UI with **custom inputs**.

### Simple Analogy
Think of it like a **form with buttons**:
- Regular triggers: Automatic (push → auto-runs)
- Workflow Dispatch: Manual (click button → fill form → run)

### Key Features:
- ✅ **Manual trigger** from GitHub Actions UI
- ✅ **Custom inputs** (text, choices, booleans)
- ✅ **On-demand execution** (run when you need it)
- ✅ **Input validation** (type checking, required fields)

---

## 🔍 Why Do We Need It?

### 1. **Manual Deployments** 🚀
- Deploy to specific environments on demand
- Choose version/tag to deploy
- Control when deployments happen

**Example:**
```
❌ WITHOUT: Auto-deploys on every push (risky!)
✅ WITH: Click "Deploy to Production" → Choose version → Deploy safely
```

### 2. **Testing & Debugging** 🐛
- Run workflows manually for testing
- Test specific scenarios with custom inputs
- Debug issues without waiting for triggers

### 3. **Flexible Operations** ⚙️
- Run maintenance tasks on demand
- Execute cleanup jobs manually
- Trigger one-off operations

### 4. **User Control** 👤
- Let users choose deployment options
- Provide choices (dev/staging/prod)
- Add safety flags (force, skip tests)

### 5. **Scheduled Operations** 📅
- Run workflows outside normal triggers
- Execute tasks at specific times
- Manual backup/restore operations

---

## ⚙️ How Does It Work?

### Step-by-Step Flow

```
1. Workflow has workflow_dispatch trigger
   ↓
2. Appears in GitHub Actions UI
   ↓
3. User clicks "Run workflow"
   ↓
4. Form appears with input fields
   ↓
5. User fills inputs and clicks "Run workflow"
   ↓
6. Workflow executes with provided inputs
   ↓
7. Inputs accessible via: github.event.inputs.input-name
```

### Visual Flow

```
GitHub Actions Tab
    │
    ▼
┌─────────────────────┐
│  Workflow Name      │
│  [Run workflow ▼]   │ ← Click here
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Input Form:        │
│  Environment: [▼]  │
│  Version: [____]    │
│  Force: [☐]         │
│  [Run workflow]     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Workflow Runs      │
│  with Inputs        │
└─────────────────────┘
```

---

## 📝 Input Types

### 1. **String Input**
```yaml
workflow_dispatch:
  inputs:
    version:
      description: 'Version to deploy'
      required: true
      type: string
      default: 'latest'
```

**Access:** `${{ github.event.inputs.version }}`

### 2. **Choice Input** (Dropdown)
```yaml
workflow_dispatch:
  inputs:
    environment:
      description: 'Target environment'
      required: true
      type: choice
      options:
        - development
        - staging
        - production
```

**Access:** `${{ github.event.inputs.environment }}`

### 3. **Boolean Input** (Checkbox)
```yaml
workflow_dispatch:
  inputs:
    force:
      description: 'Force deployment (skip tests)'
      required: false
      type: boolean
      default: false
```

**Access:** `${{ github.event.inputs.force }}`

### 4. **Environment Input**
```yaml
workflow_dispatch:
  inputs:
    environment:
      description: 'GitHub environment'
      required: true
      type: environment
```

**Access:** `${{ github.event.inputs.environment }}`

---

## 🎯 Task 11 Implementation Guide

### Requirements Recap:
1. Create `.github/workflows/manual-deploy.yml`
2. Add `workflow_dispatch` trigger with inputs:
   - `environment`: Choice (development, staging, production)
   - `version`: String (default: "latest")
   - `force`: Boolean (default: false)
3. Workflow should:
   - Print all input values
   - Deploy to selected environment
   - Use version tag if provided
   - Skip tests if `force` is true

### Complete Workflow Example:

```yaml
name: Manual Deployment

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - development
          - staging
          - production
      version:
        description: 'Version tag to deploy'
        required: false
        type: string
        default: 'latest'
      force:
        description: 'Force deployment (skip tests)'
        required: false
        type: boolean
        default: false

jobs:
  print-inputs:
    name: Print Input Values
    runs-on: ubuntu-latest
    steps:
      - name: Print all input values
        run: |
          echo "Environment: ${{ github.event.inputs.environment }}"
          echo "Version: ${{ github.event.inputs.version }}"
          echo "Force: ${{ github.event.inputs.force }}"
          echo ""
          echo "All inputs received successfully!"

  deploy:
    name: Deploy to ${{ github.event.inputs.environment }}
    runs-on: ubuntu-latest
    needs: print-inputs
    environment:
      name: ${{ github.event.inputs.environment }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Print deployment info
        run: |
          echo "🚀 Deploying to: ${{ github.event.inputs.environment }}"
          echo "📦 Version: ${{ github.event.inputs.version }}"
          echo "⚡ Force mode: ${{ github.event.inputs.force }}"
      
      - name: Run tests
        if: github.event.inputs.force != 'true'
        run: |
          echo "Running tests..."
          echo "✅ Tests passed!"
      
      - name: Skip tests (force mode)
        if: github.event.inputs.force == 'true'
        run: |
          echo "⚠️ Skipping tests (force mode enabled)"
      
      - name: Deploy to ${{ github.event.inputs.environment }}
        run: |
          echo "Deploying version ${{ github.event.inputs.version }} to ${{ github.event.inputs.environment }}..."
          echo "✅ Deployment successful!"
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
          VERSION: ${{ github.event.inputs.version }}
          ENVIRONMENT: ${{ github.event.inputs.environment }}
      
      - name: Deployment summary
        run: |
          echo "## Deployment Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Property | Value |" >> $GITHUB_STEP_SUMMARY
          echo "|----------|-------|" >> $GITHUB_STEP_SUMMARY
          echo "| Environment | ${{ github.event.inputs.environment }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Version | ${{ github.event.inputs.version }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Force Mode | ${{ github.event.inputs.force }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Status | ✅ Success |" >> $GITHUB_STEP_SUMMARY
```

### Key Points:

1. **Input Definition:**
   ```yaml
   workflow_dispatch:
     inputs:
       environment:
         type: choice
         options: [development, staging, production]
   ```

2. **Accessing Inputs:**
   ```yaml
   ${{ github.event.inputs.environment }}
   ${{ github.event.inputs.version }}
   ${{ github.event.inputs.force }}
   ```

3. **Conditional Logic:**
   ```yaml
   if: github.event.inputs.force != 'true'  # Run if force is false
   if: github.event.inputs.force == 'true'  # Run if force is true
   ```

4. **Dynamic Environment:**
   ```yaml
   environment:
     name: ${{ github.event.inputs.environment }}
   ```

---

## 💡 Common Patterns

### Pattern 1: Environment Selection
```yaml
workflow_dispatch:
  inputs:
    environment:
      type: choice
      options: [dev, staging, prod]
```

### Pattern 2: Version Tag
```yaml
workflow_dispatch:
  inputs:
    version:
      type: string
      default: 'latest'
```

### Pattern 3: Feature Flags
```yaml
workflow_dispatch:
  inputs:
    skip-tests:
      type: boolean
      default: false
    skip-build:
      type: boolean
      default: false
```

### Pattern 4: Multiple Choices
```yaml
workflow_dispatch:
  inputs:
    action:
      type: choice
      options: [deploy, rollback, restart]
    target:
      type: choice
      options: [frontend, backend, database]
```

---

## ✅ Best Practices

### 1. **Provide Defaults**
```yaml
✅ GOOD:
  version:
    default: 'latest'

❌ BAD:
  version:
    # No default - user must always provide
```

### 2. **Use Descriptive Names**
```yaml
✅ GOOD:
  target-environment:
    description: 'Target deployment environment'

❌ BAD:
  env:
    description: 'env'
```

### 3. **Validate Inputs**
```yaml
✅ GOOD:
  - name: Validate version
    run: |
      if [[ ! "${{ github.event.inputs.version }}" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Invalid version format!"
        exit 1
      fi
```

### 4. **Use Choice for Limited Options**
```yaml
✅ GOOD:
  environment:
    type: choice
    options: [dev, staging, prod]

❌ BAD:
  environment:
    type: string
    # User could type anything (typos, invalid values)
```

### 5. **Document Inputs Clearly**
```yaml
✅ GOOD:
  force:
    description: 'Skip all tests and deploy immediately (use with caution)'
    type: boolean
    default: false
```

---

## 🚨 Common Mistakes

### 1. **Wrong Input Access Syntax**
```yaml
# ❌ WRONG:
${{ inputs.environment }}

# ✅ CORRECT:
${{ github.event.inputs.environment }}
```

### 2. **Boolean Comparison**
```yaml
# ❌ WRONG:
if: github.event.inputs.force == true

# ✅ CORRECT:
if: github.event.inputs.force == 'true'
```

### 3. **Missing Default Values**
```yaml
# ❌ WRONG:
version:
  type: string
  # No default - always required

# ✅ CORRECT:
version:
  type: string
  default: 'latest'
```

### 4. **Not Using Choice Type**
```yaml
# ❌ WRONG:
environment:
  type: string
  # User can type anything

# ✅ CORRECT:
environment:
  type: choice
  options: [dev, staging, prod]
```

---

## 📊 Summary

### What is Workflow Dispatch?
- Manual trigger for workflows
- Custom inputs from GitHub UI
- On-demand execution

### Why Do We Need It?
- Manual deployments
- Testing and debugging
- Flexible operations
- User control
- Scheduled operations

### How Does It Work?
1. Define `workflow_dispatch` with inputs
2. Appears in GitHub Actions UI
3. User fills form and runs
4. Access inputs via `github.event.inputs.*`

### Key Input Types:
- `string` - Text input
- `choice` - Dropdown selection
- `boolean` - Checkbox
- `environment` - GitHub environment

---

**Ready to implement Task 11?** Use the example workflow above as a starting point! 🚀

