# 🖥️ Self-Hosted Runner Setup - Complete Guide

## 📋 Table of Contents
1. [What is a Self-Hosted Runner?](#what-is-a-self-hosted-runner)
2. [Why Do We Need It?](#why-do-we-need-it)
3. [How Does It Work?](#how-does-it-work)
4. [Task 15 Implementation Guide](#task-15-implementation-guide)
5. [Best Practices](#best-practices)

---

## 🎯 What is a Self-Hosted Runner?

A **Self-Hosted Runner** is a machine that **you control** and configure to run GitHub Actions workflows. Instead of using GitHub's hosted runners (Ubuntu, Windows, macOS), you use your own infrastructure.

### Simple Analogy
- **GitHub Hosted Runners**: Rented servers (GitHub provides)
- **Self-Hosted Runners**: Your own servers (you provide)

### Key Features:
- ✅ **Full control** over the environment
- ✅ **Custom hardware** (GPUs, specialized machines)
- ✅ **Cost savings** (for high usage)
- ✅ **Security** (data stays on your infrastructure)
- ✅ **Custom software** (pre-installed tools)

---

## 🔍 Why Do We Need It?

### 1. **Cost Savings** 💰
- GitHub Actions: Free tier limited (2000 min/month)
- Self-hosted: Unlimited (just hardware costs)
- **Good for**: High-volume workflows

### 2. **Custom Hardware** 🖥️
- GPU support for ML/AI workloads
- Specialized hardware requirements
- High-memory machines
- **Good for**: Specialized workloads

### 3. **Security & Compliance** 🔒
- Data never leaves your infrastructure
- Meet compliance requirements (HIPAA, SOC2)
- Air-gapped environments
- **Good for**: Sensitive data processing

### 4. **Performance** ⚡
- Faster builds (no cold starts)
- Pre-installed dependencies
- Custom optimizations
- **Good for**: Large projects

### 5. **Software Requirements** 📦
- Pre-installed tools
- Custom software stack
- Legacy system support
- **Good for**: Specific toolchains

---

## ⚙️ How Does It Work?

### Setup Process:

```
1. Download runner application
   ↓
2. Configure runner (token, name, labels)
   ↓
3. Install runner as service
   ↓
4. Runner connects to GitHub
   ↓
5. Runner appears in repository settings
   ↓
6. Workflows can use runner via labels
```

### Visual Flow:

```
Your Machine/Server
    │
    ▼
┌─────────────────────┐
│  Runner Application  │
│  - Connects to       │
│    GitHub            │
│  - Polls for jobs    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  GitHub Repository   │
│  - Sends jobs to    │
│    runner            │
│  - Receives results  │
└─────────────────────┘
```

---

## 🎯 Task 15 Implementation Guide

### Requirements Recap:
1. Set up a self-hosted runner (local machine or VM)
2. Create `.github/workflows/self-hosted.yml`:
   - Uses self-hosted runner
   - Labels: `self-hosted`, `linux` (or your OS)
   - Runs a test job
   - Uses runner-specific features (if any)

### Step 1: Set Up Self-Hosted Runner

#### For Linux/macOS:

```bash
# 1. Create a folder
mkdir actions-runner && cd actions-runner

# 2. Download the latest runner package
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# 3. Extract the installer
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# 4. Configure the runner
./config.sh --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN

# 5. Install as a service (optional, for auto-start)
sudo ./svc.sh install
sudo ./svc.sh start
```

#### For Windows:

```powershell
# 1. Create a folder
mkdir actions-runner; cd actions-runner

# 2. Download the latest runner package
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-win-x64-2.311.0.zip -OutFile actions-runner-win-x64-2.311.0.zip

# 3. Extract the installer
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD\actions-runner-win-x64-2.311.0.zip", "$PWD")

# 4. Configure the runner
.\config.cmd --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN

# 5. Install as a service (optional)
.\svc.cmd install
.\svc.cmd start
```

#### Getting the Token:

1. Go to your repository on GitHub
2. **Settings** → **Actions** → **Runners**
3. Click **"New self-hosted runner"**
4. Copy the token from the setup instructions

### Step 2: Create Workflow Using Self-Hosted Runner

```yaml
# .github/workflows/self-hosted.yml
name: Self-Hosted Runner Test

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  workflow_dispatch:

jobs:
  test-self-hosted:
    name: Test on Self-Hosted Runner
    runs-on: self-hosted  # Use self-hosted runner
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Display runner information
        run: |
          echo "🏃 Runner Information:"
          echo "Runner OS: $(uname -s)"
          echo "Runner Architecture: $(uname -m)"
          echo "Runner Hostname: $(hostname)"
          echo "Runner User: $(whoami)"
          echo "Current Directory: $(pwd)"
          echo "Runner Labels: ${{ runner.labels }}"
      
      - name: Check runner environment
        run: |
          echo "📦 Environment Check:"
          echo "Python version:"
          python3 --version || echo "Python not installed"
          echo "Node version:"
          node --version || echo "Node not installed"
          echo "Docker version:"
          docker --version || echo "Docker not installed"
      
      - name: Run test job
        run: |
          echo "🧪 Running test job on self-hosted runner..."
          echo "This job runs on your own infrastructure!"
          echo "✅ Test completed successfully!"
      
      - name: Use runner-specific features
        run: |
          echo "🔧 Using runner-specific features..."
          # Example: Access local files, custom tools, etc.
          echo "Runner has access to local filesystem"
          ls -la
          echo "✅ Runner-specific features work!"

  test-with-labels:
    name: Test with Specific Labels
    runs-on: [self-hosted, linux]  # Use labels to target specific runner
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Verify labels
        run: |
          echo "Runner labels: ${{ runner.labels }}"
          echo "Expected: self-hosted, linux"
          echo "✅ Running on labeled runner!"
```

### Step 3: Configure Runner Labels (Optional)

When configuring the runner, you can add custom labels:

```bash
# During config.sh, you'll be asked:
Enter the name of the runner group to add this runner to: [press Enter for Default]
Enter the name of the runner: [enter name, e.g., "my-linux-runner"]
Enter any additional labels: [enter labels, e.g., "linux, gpu, custom"]
```

Or add labels later:
```bash
./config.sh --labels "linux,gpu,custom"
```

---

## ✅ Best Practices

### 1. **Security** 🔒
```yaml
✅ GOOD:
  - Use dedicated machines for runners
  - Limit repository access
  - Use runner groups for organization

❌ BAD:
  - Use personal machines with sensitive data
  - Give runners access to all repositories
```

### 2. **Labels** 🏷️
```yaml
✅ GOOD:
  runs-on: [self-hosted, linux, gpu]

❌ BAD:
  runs-on: self-hosted
  # No labels - might run on wrong runner
```

### 3. **Service Installation** 🔧
```yaml
✅ GOOD:
  - Install runner as service
  - Auto-start on boot
  - Monitor runner status

❌ BAD:
  - Run manually each time
  - No monitoring
```

### 4. **Resource Management** 💻
```yaml
✅ GOOD:
  - Limit concurrent jobs
  - Monitor resource usage
  - Scale as needed

❌ BAD:
  - Run unlimited jobs
  - No resource monitoring
```

### 5. **Updates** 🔄
```yaml
✅ GOOD:
  - Keep runner updated
  - Monitor for security updates
  - Test updates before production

❌ BAD:
  - Never update runner
  - Ignore security patches
```

---

## 🚨 Important Considerations

### Security Warnings:

1. **⚠️ Self-hosted runners execute code from workflows**
   - Only use trusted repositories
   - Isolate runners from sensitive systems

2. **⚠️ Workflows can access secrets**
   - Limit secret access
   - Use least-privilege principle

3. **⚠️ Runners can access network**
   - Use firewalls
   - Monitor network traffic

### Best Practices:

- ✅ Use dedicated VMs/machines
- ✅ Isolate from production systems
- ✅ Regular security updates
- ✅ Monitor runner activity
- ✅ Use runner groups for organization

---

## 📊 Summary

### What is a Self-Hosted Runner?
- Machine you control to run GitHub Actions
- Alternative to GitHub-hosted runners
- Full control over environment

### Why Do We Need It?
- Cost savings
- Custom hardware
- Security & compliance
- Performance
- Software requirements

### How Does It Work?
1. Download runner application
2. Configure with token
3. Install as service
4. Runner polls for jobs
5. Execute workflows

### Key Syntax:
```yaml
runs-on: self-hosted
# or
runs-on: [self-hosted, linux, custom-label]
```

---

## 🔗 Resources

- [GitHub Docs: Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Runner Releases](https://github.com/actions/runner/releases)
- [Runner Configuration](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners)

---

**Ready to implement Task 15?** Follow the setup steps above! 🚀

**Note**: This task requires setting up a physical machine or VM, so it's optional for learning purposes.

