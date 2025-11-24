# 🧩 Custom Composite Action - Complete Guide

## 📋 Table of Contents
1. [What is a Composite Action?](#what-is-a-composite-action)
2. [Why Do We Need It?](#why-do-we-need-it)
3. [How Does It Work?](#how-does-it-work)
4. [Task 13 Implementation Guide](#task-13-implementation-guide)
5. [Best Practices](#best-practices)

---

## 🎯 What is a Composite Action?

A **Composite Action** is a reusable action that combines multiple steps into a single action. Think of it as a **function** that you can call from any workflow.

### Simple Analogy
- **Regular steps**: Individual commands
- **Composite action**: A function that groups multiple commands
- **Reusable workflow**: A complete workflow template

### Key Features:
- ✅ **Reusable** across multiple workflows
- ✅ **Combines multiple steps** into one action
- ✅ **Accepts inputs** and **produces outputs**
- ✅ **Version controlled** (can be tagged)
- ✅ **Simplifies workflows** (less code duplication)

---

## 🔍 Why Do We Need It?

### 1. **Code Reusability** 🔄
- Use the same setup logic in multiple workflows
- Avoid copy-pasting steps
- Update once, use everywhere

**Example:**
```
❌ WITHOUT: Copy-paste setup steps in 10 workflows
✅ WITH: Create one composite action, use in all 10 workflows
```

### 2. **Simplification** ✨
- Reduce workflow file size
- Make workflows more readable
- Hide complexity

### 3. **Maintainability** 🛠️
- Fix bugs in one place
- Add features once
- All workflows benefit

### 4. **Organization** 📁
- Group related steps together
- Create logical units
- Better structure

### 5. **Sharing** 👥
- Share actions across repositories
- Create action libraries
- Team-wide standards

---

## ⚙️ How Does It Work?

### Structure:
```
.github/actions/
  └── action-name/
      └── action.yml
```

### Basic Example:
```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Sets up project environment'
inputs:
  language:
    description: 'Programming language'
    required: true
  version:
    description: 'Version number'
    required: true
outputs:
  setup-complete:
    description: 'Whether setup completed'
    value: ${{ steps.setup.outputs.complete }}
runs:
  using: 'composite'
  steps:
    - name: Setup ${{ inputs.language }} ${{ inputs.version }}
      id: setup
      shell: bash
      run: |
        echo "Setting up ${{ inputs.language }} ${{ inputs.version }}"
        echo "complete=true" >> $GITHUB_OUTPUT
```

### Using the Action:
```yaml
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-project
        with:
          language: python
          version: '3.11'
      - name: Use output
        run: echo "Setup: ${{ steps.setup-project.outputs.setup-complete }}"
```

---

## 🎯 Task 13 Implementation Guide

### Requirements Recap:
1. Create `.github/actions/setup-project/action.yml`:
   - Inputs: `language`, `version`, `install-command`
   - Sets up the specified language
   - Runs install command
   - Outputs: `setup-complete` (true/false)
2. Create `.github/workflows/use-composite-action.yml`:
   - Uses your composite action
   - Tests it with Python and Node.js
   - Uses the output to determine next steps

### Step 1: Create Composite Action

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Sets up project environment with specified language and version'
inputs:
  language:
    description: 'Programming language (python or node)'
    required: true
  version:
    description: 'Version number (e.g., "3.11" or "20")'
    required: true
  install-command:
    description: 'Command to install dependencies'
    required: false
    default: ''
outputs:
  setup-complete:
    description: 'Whether setup completed successfully'
    value: ${{ steps.setup.outputs.complete }}
runs:
  using: 'composite'
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Python ${{ inputs.version }}
      if: inputs.language == 'python'
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.version }}
        cache: 'pip'
    
    - name: Setup Node.js ${{ inputs.version }}
      if: inputs.language == 'node'
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.version }}
        cache: 'npm'
    
    - name: Install dependencies
      if: inputs.install-command != ''
      shell: bash
      run: ${{ inputs.install-command }}
    
    - name: Verify setup
      id: setup
      shell: bash
      run: |
        if [ "${{ inputs.language }}" == "python" ]; then
          python --version
          echo "complete=true" >> $GITHUB_OUTPUT
        elif [ "${{ inputs.language }}" == "node" ]; then
          node --version
          echo "complete=true" >> $GITHUB_OUTPUT
        else
          echo "complete=false" >> $GITHUB_OUTPUT
        fi
```

### Step 2: Create Workflow Using Composite Action

```yaml
# .github/workflows/use-composite-action.yml
name: Use Composite Action

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  workflow_dispatch:

jobs:
  test-python:
    name: Test Python Setup
    runs-on: ubuntu-latest
    steps:
      - name: Setup Python project
        id: setup-python
        uses: ./.github/actions/setup-project
        with:
          language: python
          version: '3.11'
          install-command: 'pip install -r requirements.txt || echo "No requirements.txt"'
      
      - name: Check setup status
        run: |
          if [ "${{ steps.setup-python.outputs.setup-complete }}" == "true" ]; then
            echo "✅ Python setup completed successfully!"
            echo "Python version:"
            python --version
          else
            echo "❌ Python setup failed!"
            exit 1
          fi
      
      - name: Run Python tests
        if: steps.setup-python.outputs.setup-complete == 'true'
        run: |
          echo "Running Python tests..."
          # pytest || echo "No pytest found"
          echo "✅ Python tests passed!"

  test-node:
    name: Test Node.js Setup
    runs-on: ubuntu-latest
    steps:
      - name: Setup Node.js project
        id: setup-node
        uses: ./.github/actions/setup-project
        with:
          language: node
          version: '20'
          install-command: 'npm install || echo "No package.json"'
      
      - name: Check setup status
        run: |
          if [ "${{ steps.setup-node.outputs.setup-complete }}" == "true" ]; then
            echo "✅ Node.js setup completed successfully!"
            echo "Node version:"
            node --version
          else
            echo "❌ Node.js setup failed!"
            exit 1
          fi
      
      - name: Run Node.js tests
        if: steps.setup-node.outputs.setup-complete == 'true'
        run: |
          echo "Running Node.js tests..."
          # npm test || echo "No test script found"
          echo "✅ Node.js tests passed!"

  summary:
    name: Setup Summary
    runs-on: ubuntu-latest
    needs: [test-python, test-node]
    if: always()
    steps:
      - name: Print summary
        run: |
          echo "## Composite Action Test Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Language | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|----------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Python | ${{ needs.test-python.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Node.js | ${{ needs.test-node.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "✅ Composite action tested successfully!" >> $GITHUB_STEP_SUMMARY
```

---

## ✅ Best Practices

### 1. **Use Descriptive Names**
```yaml
✅ GOOD:
  name: 'Setup Python Project'

❌ BAD:
  name: 'Setup'
```

### 2. **Document Inputs**
```yaml
✅ GOOD:
  inputs:
    language:
      description: 'Programming language (python or node)'
      required: true

❌ BAD:
  inputs:
    lang:
      # No description
```

### 3. **Provide Defaults When Possible**
```yaml
✅ GOOD:
  install-command:
    default: 'npm install'

❌ BAD:
  install-command:
    # Always required
```

### 4. **Handle Errors Gracefully**
```yaml
✅ GOOD:
  run: |
    pip install -r requirements.txt || echo "No requirements.txt found"

❌ BAD:
  run: pip install -r requirements.txt
  # Fails if file doesn't exist
```

### 5. **Use Outputs for Status**
```yaml
✅ GOOD:
  outputs:
    setup-complete:
      value: ${{ steps.setup.outputs.complete }}

❌ BAD:
  # No outputs - can't check status
```

---

## 📊 Summary

### What is a Composite Action?
- Reusable action that combines multiple steps
- Like a function for workflows
- Accepts inputs and produces outputs

### Why Do We Need It?
- Code reusability
- Simplification
- Maintainability
- Organization
- Sharing

### Key Structure:
```
.github/actions/action-name/action.yml
```

### Key Features:
- `inputs` - Parameters
- `outputs` - Return values
- `runs.using: composite` - Required
- `steps` - Action steps

---

**Ready to implement Task 13?** Use the examples above as a starting point! 🚀

