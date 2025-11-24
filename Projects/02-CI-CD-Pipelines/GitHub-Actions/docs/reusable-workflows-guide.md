# 🔄 Reusable Workflows in GitHub Actions - Complete Guide

## 🎯 What is a Reusable Workflow?

A **reusable workflow** is a workflow that can be called from other workflows. Think of it as a **function** or **template** that you can reuse across multiple workflows to avoid code duplication.

### Simple Analogy
- **Regular workflow**: A complete script that runs independently
- **Reusable workflow**: A function that can be called from other scripts with different parameters

---

## 🧠 Core Concepts

### 1. **workflow_call Trigger**
The special trigger that makes a workflow reusable:

```yaml
on:
  workflow_call:  # This makes the workflow reusable
    inputs:
      # Define inputs here
    secrets:
      # Define secrets here
    outputs:
      # Define outputs here
```

**Key Point**: A reusable workflow **cannot** have other triggers (like `push`, `pull_request`) - it can **only** be called by other workflows.

### 2. **Inputs**
Parameters you pass TO the reusable workflow:

```yaml
on:
  workflow_call:
    inputs:
      language:
        description: 'Programming language'
        required: true
        type: string
      version:
        description: 'Version number'
        required: false
        type: string
        default: 'latest'
```

**Input Types:**
- `string` - Text value
- `number` - Numeric value
- `boolean` - True/false
- `choice` - Select from options
- `environment` - Environment name

### 3. **Secrets**
Sensitive data passed to the reusable workflow:

```yaml
on:
  workflow_call:
    secrets:
      API_KEY:
        required: true
      DEPLOY_TOKEN:
        required: false
```

**Important**: Secrets must be explicitly passed from the calling workflow.

### 4. **Outputs**
Values returned FROM the reusable workflow:

```yaml
on:
  workflow_call:
    outputs:
      test-status:
        description: 'Test execution status'
        value: ${{ jobs.test.outputs.status }}
      build-status:
        description: 'Build execution status'
        value: ${{ jobs.build.outputs.status }}
```

**Key Point**: Outputs reference job outputs, not step outputs directly.

---

## 📝 Basic Structure

### Reusable Workflow (The Template)

```yaml
name: Reusable Build and Test

on:
  workflow_call:
    inputs:
      language:
        description: 'Programming language (python or node)'
        required: true
        type: choice
        options:
          - python
          - node
      version:
        description: 'Version number'
        required: true
        type: string
    outputs:
      test-status:
        description: 'Test execution status'
        value: ${{ jobs.test.outputs.status }}

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      status: ${{ steps.test-result.outputs.status }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
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
      
      - name: Run tests
        id: test-result
        run: |
          if [ "${{ inputs.language }}" == "python" ]; then
            pytest
          else
            npm test
          fi
          echo "status=success" >> $GITHUB_OUTPUT
```

### Calling Workflow (The User)

```yaml
name: Main Workflow

on:
  push:
    branches: [main]

jobs:
  test-python:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: python
      version: '3.11'
  
  test-node:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: node
      version: '20'
  
  print-results:
    needs: [test-python, test-node]
    runs-on: ubuntu-latest
    steps:
      - name: Print Python test status
        run: echo "Python tests: ${{ needs.test-python.outputs.test-status }}"
      
      - name: Print Node test status
        run: echo "Node tests: ${{ needs.test-node.outputs.test-status }}"
```

---

## 🔍 How It Works

### Step-by-Step Flow

1. **Main workflow triggers** (e.g., on push)
2. **Main workflow calls reusable workflow** with inputs
3. **Reusable workflow executes** using the provided inputs
4. **Reusable workflow produces outputs** from its jobs
5. **Main workflow receives outputs** via `needs.<job-id>.outputs.<output-name>`

### Visual Flow

```
Main Workflow
    │
    ├─> Calls Reusable Workflow (with inputs)
    │       │
    │       ├─> Executes jobs
    │       │
    │       └─> Returns outputs
    │
    └─> Uses outputs in subsequent jobs
```

---

## 💡 Key Benefits

### 1. **DRY Principle** (Don't Repeat Yourself)
Instead of copying the same workflow code multiple times:

```yaml
# ❌ BAD: Duplicated code
jobs:
  test-python-3.9:
    # ... 50 lines of setup and test code ...
  test-python-3.10:
    # ... 50 lines of setup and test code ... (duplicated!)
  test-python-3.11:
    # ... 50 lines of setup and test code ... (duplicated!)
```

```yaml
# ✅ GOOD: Reusable workflow
jobs:
  test-python-3.9:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: python
      version: '3.9'
  test-python-3.10:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: python
      version: '3.10'
  test-python-3.11:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: python
      version: '3.11'
```

### 2. **Centralized Maintenance**
Update the reusable workflow once, and all calling workflows benefit:

```yaml
# Update test command in one place
# All 10 workflows using it automatically get the update!
```

### 3. **Consistency**
Ensures all workflows use the same standardized process.

### 4. **Organization**
Keeps workflows clean and focused on their specific purpose.

---

## 📚 Complete Example

### Reusable Workflow: `build-and-test.yml`

```yaml
name: Reusable Build and Test

on:
  workflow_call:
    inputs:
      language:
        description: 'Programming language (python or node)'
        required: true
        type: choice
        options:
          - python
          - node
      version:
        description: 'Version number (e.g., "3.11" or "20")'
        required: true
        type: string
    outputs:
      test-status:
        description: 'Test execution status (success/failure)'
        value: ${{ jobs.test.outputs.status }}

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      status: ${{ steps.test-result.outputs.status }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python ${{ inputs.version }}
        if: inputs.language == 'python'
        uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.version }}
          cache: 'pip'
      
      - name: Set up Node.js ${{ inputs.version }}
        if: inputs.language == 'node'
        uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: |
          if [ "${{ inputs.language }}" == "python" ]; then
            pip install -r requirements.txt
          else
            npm ci
          fi
      
      - name: Run tests
        id: test-result
        run: |
          if [ "${{ inputs.language }}" == "python" ]; then
            pytest || echo "status=failure" >> $GITHUB_OUTPUT
          else
            npm test || echo "status=failure" >> $GITHUB_OUTPUT
          fi
          if [ "$?" == "0" ]; then
            echo "status=success" >> $GITHUB_OUTPUT
          fi
```

### Calling Workflow: `use-reusable.yml`

```yaml
name: Use Reusable Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-python:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: python
      version: '3.11'
  
  test-node:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: node
      version: '20'
  
  print-results:
    needs: [test-python, test-node]
    runs-on: ubuntu-latest
    steps:
      - name: Print Python test status
        run: |
          echo "Python 3.11 test status: ${{ needs.test-python.outputs.test-status }}"
      
      - name: Print Node test status
        run: |
          echo "Node.js 20 test status: ${{ needs.test-node.outputs.test-status }}"
```

---

## 🔑 Important Rules

### 1. **File Location**
- Reusable workflows can be in any `.github/workflows/` directory
- Common practice: `.github/workflows/reusable/` subdirectory

### 2. **Path Reference**
```yaml
# Same repository
uses: ./.github/workflows/reusable/build-and-test.yml

# Different repository (same organization)
uses: .github/workflows/reusable/build-and-test.yml@main

# Different repository (external)
uses: owner/repo/.github/workflows/build-and-test.yml@v1
```

### 3. **Input Access**
In the reusable workflow, access inputs with:
```yaml
${{ inputs.input-name }}
```

### 4. **Output Access**
In the calling workflow, access outputs with:
```yaml
${{ needs.job-id.outputs.output-name }}
```

### 5. **Secrets Must Be Explicit**
```yaml
# Calling workflow
jobs:
  deploy:
    uses: ./.github/workflows/reusable/deploy.yml
    secrets:
      API_KEY: ${{ secrets.API_KEY }}  # Must explicitly pass
```

### 6. **No Direct Triggers**
Reusable workflows **cannot** have:
- `push`
- `pull_request`
- `schedule`
- `workflow_dispatch`

They **can only** have `workflow_call`.

---

## 🎓 Advanced Patterns

### 1. **Conditional Logic Based on Inputs**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
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

### 2. **Multiple Outputs**

```yaml
on:
  workflow_call:
    outputs:
      test-status:
        value: ${{ jobs.test.outputs.status }}
      build-status:
        value: ${{ jobs.build.outputs.status }}
      coverage:
        value: ${{ jobs.test.outputs.coverage }}
```

### 3. **Required vs Optional Inputs**

```yaml
on:
  workflow_call:
    inputs:
      language:
        required: true  # Must be provided
        type: string
      version:
        required: false  # Optional
        type: string
        default: 'latest'  # Default value if not provided
```

### 4. **Choice Input Type**

```yaml
on:
  workflow_call:
    inputs:
      environment:
        type: choice
        options:
          - development
          - staging
          - production
        required: true
```

### 5. **Job Dependencies in Reusable Workflows**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    # ... test steps ...
  
  build:
    needs: test  # Wait for test to complete
    runs-on: ubuntu-latest
    # ... build steps ...
```

---

## ⚠️ Common Mistakes

### 1. **Trying to Use Regular Triggers**
```yaml
# ❌ WRONG: Can't have push trigger
on:
  push:
    branches: [main]
  workflow_call:  # This won't work!
```

```yaml
# ✅ CORRECT: Only workflow_call
on:
  workflow_call:
    inputs:
      # ...
```

### 2. **Wrong Output Reference**
```yaml
# ❌ WRONG: Can't reference step outputs directly
outputs:
  test-status:
    value: ${{ steps.test.outputs.status }}  # Wrong!

# ✅ CORRECT: Must reference job outputs
outputs:
  test-status:
    value: ${{ jobs.test.outputs.status }}  # Correct!
```

### 3. **Forgetting to Pass Secrets**
```yaml
# ❌ WRONG: Secrets not passed
jobs:
  deploy:
    uses: ./.github/workflows/reusable/deploy.yml
    with:
      environment: production
    # Missing secrets!

# ✅ CORRECT: Secrets explicitly passed
jobs:
  deploy:
    uses: ./.github/workflows/reusable/deploy.yml
    with:
      environment: production
    secrets:
      API_KEY: ${{ secrets.API_KEY }}
```

### 4. **Wrong Path Reference**
```yaml
# ❌ WRONG: Missing leading ./
uses: .github/workflows/reusable/build.yml

# ✅ CORRECT: Use ./
uses: ./.github/workflows/reusable/build.yml
```

---

## 📊 Comparison: Reusable vs Regular Workflow

| Feature | Regular Workflow | Reusable Workflow |
|---------|-----------------|-------------------|
| Triggers | `push`, `pull_request`, `schedule`, etc. | Only `workflow_call` |
| Can be called | No | Yes, by other workflows |
| Inputs | No | Yes, via `workflow_call.inputs` |
| Outputs | No | Yes, via `workflow_call.outputs` |
| Secrets | Direct access | Must be passed explicitly |
| Use case | Standalone automation | Shared logic/templates |

---

## ✅ Best Practices

### 1. **Use Descriptive Names**
```yaml
# ✅ GOOD
name: Reusable Build and Test Workflow

# ❌ BAD
name: Workflow
```

### 2. **Document Inputs**
```yaml
inputs:
  language:
    description: 'Programming language (python or node)'  # Clear description
    required: true
    type: choice
    options:
      - python
      - node
```

### 3. **Provide Defaults When Possible**
```yaml
inputs:
  version:
    required: false
    type: string
    default: 'latest'  # Makes it easier to use
```

### 4. **Organize in Subdirectories**
```
.github/workflows/
  ├── ci.yml              # Main workflows
  ├── deploy.yml
  └── reusable/           # Reusable workflows
      ├── build-and-test.yml
      └── deploy.yml
```

### 5. **Handle Errors Gracefully**
```yaml
steps:
  - name: Run tests
    id: test-result
    run: |
      pytest || echo "status=failure" >> $GITHUB_OUTPUT
      if [ "$?" == "0" ]; then
        echo "status=success" >> $GITHUB_OUTPUT
      fi
```

---

## 🎯 Task 9 Implementation Guide

For your specific task, here's what you need:

### 1. Create Reusable Workflow: `.github/workflows/reusable/build-and-test.yml`

```yaml
name: Reusable Build and Test

on:
  workflow_call:
    inputs:
      language:
        description: 'Programming language (python or node)'
        required: true
        type: choice
        options:
          - python
          - node
      version:
        description: 'Version number (e.g., "3.11" or "20")'
        required: true
        type: string
    outputs:
      test-status:
        description: 'Test execution status (success/failure)'
        value: ${{ jobs.test.outputs.status }}

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      status: ${{ steps.test-result.outputs.status }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python ${{ inputs.version }}
        if: inputs.language == 'python'
        uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.version }}
      
      - name: Set up Node.js ${{ inputs.version }}
        if: inputs.language == 'node'
        uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.version }}
      
      - name: Install dependencies
        run: |
          if [ "${{ inputs.language }}" == "python" ]; then
            pip install -r requirements.txt
          else
            npm ci
          fi
      
      - name: Run test command
        id: test-result
        run: |
          if [ "${{ inputs.language }}" == "python" ]; then
            pytest || echo "status=failure" >> $GITHUB_OUTPUT
          else
            npm test || echo "status=failure" >> $GITHUB_OUTPUT
          fi
          if [ "$?" == "0" ]; then
            echo "status=success" >> $GITHUB_OUTPUT
          fi
```

### 2. Create Calling Workflow: `.github/workflows/use-reusable.yml`

```yaml
name: Use Reusable Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-python:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: python
      version: '3.11'
  
  test-node:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      language: node
      version: '20'
  
  print-results:
    needs: [test-python, test-node]
    runs-on: ubuntu-latest
    steps:
      - name: Print Python test status
        run: echo "Python 3.11 test status: ${{ needs.test-python.outputs.test-status }}"
      
      - name: Print Node test status
        run: echo "Node.js 20 test status: ${{ needs.test-node.outputs.test-status }}"
```

---

## 📚 Summary

**Key Takeaways:**
1. ✅ Reusable workflows use `workflow_call` trigger
2. ✅ They accept `inputs` and return `outputs`
3. ✅ They can be called from other workflows using `uses:`
4. ✅ They help avoid code duplication (DRY principle)
5. ✅ They enable centralized maintenance
6. ✅ Secrets must be explicitly passed
7. ✅ Outputs are accessed via `needs.<job-id>.outputs.<output-name>`

**Remember**: Reusable workflows are like functions - define once, use many times! 🚀

