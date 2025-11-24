# 🎯 GitHub Actions Practice Tasks

Progressive tasks to master GitHub Actions. Complete each task and I'll validate your work by commenting directly in your workflow files!

---

## 📋 Task Structure

Each task includes:
- **Objective**: What you need to build
- **Requirements**: Specific criteria
- **Validation**: How to check if it's correct
- **Hints**: Helpful tips (if needed)

**Validation Method**: I'll add comments directly in your workflow files showing what's good ✅ and what needs fixing ⚠️, plus a validation summary at the bottom of each file.

---

## 🟢 Beginner Tasks

### Task 1: Hello World Workflow ⭐

**Objective**: Create your first GitHub Actions workflow

**Requirements**:
1. Create `.github/workflows/hello-world.yml`
2. Name it "Hello World Workflow"
3. Trigger on push to `master` branch
4. Create one job that prints "Hello, GitHub Actions!"
5. Add a step that prints the current date/time

**Validation Checklist**:
- [ ] Workflow file exists in `.github/workflows/`
- [ ] Workflow name is "Hello World Workflow"
- [ ] Triggers on push to master
- [ ] Prints "Hello, GitHub Actions!"
- [ ] Prints current date/time
- [ ] Workflow runs successfully in GitHub Actions

**Expected Output**:
```
Hello, GitHub Actions!
Current date: 2025-01-18 10:30:00
```

---

### Task 2: Multi-Step Job ⭐

**Objective**: Create a workflow with multiple steps

**Requirements**:
1. Create `.github/workflows/multi-step.yml`
2. One job with 5 steps:
   - Step 1: Checkout code
   - Step 2: Print "Step 2: Setting up environment"
   - Step 3: Print "Step 3: Installing dependencies"
   - Step 4: Print "Step 4: Running tests"
   - Step 5: Print "Step 5: Build complete!"
3. Each step should have a descriptive name
4. Trigger on push and pull_request

**Validation Checklist**:
- [ ] Workflow has exactly 5 steps
- [ ] All steps have descriptive names
- [ ] Steps execute in order
- [ ] Triggers on both push and PR
- [ ] All steps complete successfully

---

### Task 3: Matrix Build - OS Testing ⭐⭐

**Objective**: Test your code on multiple operating systems

**Requirements**:
1. Create `.github/workflows/matrix-os.yml`
2. Use matrix strategy to test on:
   - ubuntu-latest
   - windows-latest
   - macos-latest
3. Each job should:
   - Print the OS name
   - Print the runner OS
   - Print "Tests passed on [OS]"
4. Job name should include the OS

**Validation Checklist**:
- [ ] Matrix includes all 3 OS
- [ ] Creates 3 separate jobs
- [ ] Each job prints OS-specific information
- [ ] Job names include OS (e.g., "Test on ubuntu-latest")
- [ ] All jobs run in parallel

**Expected Output** (3 jobs):
```
Job 1: Test on ubuntu-latest
  OS: Linux
  Tests passed on ubuntu-latest

Job 2: Test on windows-latest
  OS: Windows
  Tests passed on windows-latest

Job 3: Test on macos-latest
  OS: macOS
  Tests passed on macos-latest
```

---

### Task 4: Conditional Steps ⭐⭐

**Objective**: Use conditional logic in workflows

**Requirements**:
1. Create `.github/workflows/conditional.yml`
2. Trigger on push to any branch
3. Create one job with steps:
   - Step 1: Print current branch name
   - Step 2: Only run if branch is `master` - Print "This is the master branch"
   - Step 3: Only run if branch is NOT `master` - Print "This is NOT the master branch"
   - Step 4: Always run - Print "This step always runs"

**Validation Checklist**:
- [ ] Step 2 only runs on master branch
- [ ] Step 3 only runs on non-master branches
- [ ] Step 4 always runs
- [ ] Uses `if:` conditions correctly
- [ ] Test on both master and another branch

---

## 🟡 Intermediate Tasks

### Task 5: Job Dependencies ⭐⭐⭐

**Objective**: Create jobs that depend on each other

**Requirements**:
1. Create `.github/workflows/dependencies.yml`
2. Create 3 jobs:
   - `setup`: Prints "Setting up environment"
   - `test`: Depends on `setup`, prints "Running tests"
   - `deploy`: Depends on `test`, prints "Deploying application"
3. Jobs should run sequentially (setup → test → deploy)
4. Add a step in `test` that creates a file `test-results.txt`
5. `deploy` job should download and display the file

**Validation Checklist**:
- [ ] `test` job waits for `setup` to complete
- [ ] `deploy` job waits for `test` to complete
- [ ] `test` creates `test-results.txt` file
- [ ] `deploy` downloads and displays the file
- [ ] Jobs run in correct order (not parallel)

---

### Task 6: Artifacts Upload/Download ⭐⭐⭐

**Objective**: Upload and download artifacts between jobs

**Requirements**:
1. Create `.github/workflows/artifacts.yml`
2. Job 1: `build`
   - Creates a file `build-output.txt` with content "Build successful at [timestamp]"
   - Uploads it as artifact named "build-artifact"
3. Job 2: `deploy`
   - Depends on `build`
   - Downloads the artifact
   - Prints the contents of `build-output.txt`
   - Creates a new file `deploy-log.txt` with "Deployed at [timestamp]"
   - Uploads it as artifact named "deploy-artifact"

**Validation Checklist**:
- [ ] `build` job creates and uploads artifact
- [ ] `deploy` job downloads artifact successfully
- [ ] `deploy` can read the file contents
- [ ] Both artifacts are visible in GitHub Actions UI
- [ ] Artifacts have correct names

---

### Task 7: Caching Dependencies ⭐⭐⭐

**Objective**: Implement caching to speed up workflows

**📚 Learning Resources**:
- 📖 **Complete Guide**: See [`docs/caching-dependencies-guide.md`](docs/caching-dependencies-guide.md) for comprehensive concepts and examples
- 💡 **Example Workflow**: See [`examples/caching-example.yml`](examples/caching-example.yml) for reference implementation

**Key Concepts to Learn**:
- **Cache Key**: Unique identifier based on dependency file hash
- **Cache Path**: Directory where dependencies are stored
- **Cache Hit vs Miss**: Understanding when cache is used vs created
- **Restore Keys**: Fallback strategy for partial cache matches
- **Performance Impact**: Caching can save 80-90% of installation time!

**Requirements**:
1. Create `.github/workflows/caching.yml`
2. Set up Python environment
3. Create a cache for pip packages:
   - Cache key based on `requirements.txt` hash
   - Cache path: `~/.cache/pip`
4. Install dependencies from `requirements.txt`
5. Print cache hit/miss status
6. Run workflow twice to verify cache works

**Validation Checklist**:
- [ ] Cache is created with correct key
- [ ] Cache path is correct
- [ ] First run: Cache miss (expected)
- [ ] Second run: Cache hit (faster)
- [ ] Cache key uses hash of requirements.txt

**Hint**: Use `hashFiles('requirements.txt')` for cache key

---

### Task 8: Matrix with Multiple Variables ⭐⭐⭐

**Objective**: Create complex matrix builds

**Requirements**:
1. Create `.github/workflows/matrix-complex.yml`
2. Matrix with:
   - `python-version`: ['3.9', '3.10', '3.11']
   - `os`: ['ubuntu-latest', 'windows-latest']
3. Exclude: Windows with Python 3.9
4. Include: Ubuntu with Python 3.11 and `test-suite: full`
5. Each job should:
   - Print Python version
   - Print OS
   - Print test suite type (if specified)
6. Job name should include both version and OS

**Validation Checklist**:
- [ ] Matrix creates correct number of jobs (should be 5: 3.9/ubuntu, 3.10/ubuntu, 3.10/windows, 3.11/ubuntu, 3.11/windows)
- [ ] Windows + Python 3.9 is excluded
- [ ] Ubuntu + Python 3.11 has `test-suite: full`
- [ ] Job names are descriptive
- [ ] All combinations print correct information

---

## 🟠 Advanced Tasks

### Task 9: Reusable Workflow ⭐⭐⭐⭐

**Objective**: Create and use a reusable workflow

**📚 Learning Resources**:
- 📖 **Complete Guide**: See [`docs/reusable-workflows-guide.md`](docs/reusable-workflows-guide.md) for comprehensive concepts and examples
- 💡 **Example Workflows**: See [`workflows/reusable/build-and-test.yml`](workflows/reusable/build-and-test.yml) and [`workflows/06-using-reusable-workflows.yml`](workflows/06-using-reusable-workflows.yml)

**Key Concepts to Learn**:
- **workflow_call**: The trigger that makes a workflow reusable
- **Inputs**: Parameters passed TO the reusable workflow
- **Outputs**: Values returned FROM the reusable workflow
- **DRY Principle**: Don't Repeat Yourself - centralize common logic
- **Reusability**: Write once, use many times across workflows

**Requirements**:
1. Create `.github/workflows/reusable/build-and-test.yml`:
   - Accepts input: `language` (python or node)
   - Accepts input: `version` (e.g., "3.11" or "20")
   - Sets up the specified language/version
   - Runs a test command
   - Outputs: `test-status` (success/failure)
2. Create `.github/workflows/use-reusable.yml`:
   - Calls the reusable workflow twice:
     - Once for Python 3.11
     - Once for Node.js 20
   - Prints the test status from each call

**Validation Checklist**:
- [ ] Reusable workflow accepts inputs correctly
- [ ] Reusable workflow sets up correct language/version
- [ ] Reusable workflow outputs test status
- [ ] Main workflow calls reusable workflow twice
- [ ] Main workflow receives and uses outputs
- [ ] Both calls execute successfully

---

### Task 10: Environment Protection ⭐⭐⭐⭐

**Objective**: Use GitHub environments with protection rules

**Requirements**:
1. Create `.github/workflows/environment-deploy.yml`
2. Create 3 jobs:
   - `deploy-dev`: Deploys to "development" environment (no protection)
   - `deploy-staging`: Deploys to "staging" environment
   - `deploy-prod`: Deploys to "production" environment (requires approval)
3. Each job should:
   - Print the environment name
   - Print deployment status
   - Use environment-specific secrets (create dummy secrets)
4. `deploy-prod` should only run on `master` branch

**Validation Checklist**:
- [ ] All 3 environments are configured
- [ ] `deploy-dev` runs without approval
- [ ] `deploy-staging` may require approval (if configured)
- [ ] `deploy-prod` requires manual approval
- [ ] `deploy-prod` only runs on master branch
- [ ] Each job uses correct environment

**Note**: You'll need to configure environments in GitHub Settings → Environments

---

### Task 11: Workflow Dispatch with Inputs ⭐⭐⭐⭐

**Objective**: Create a workflow that accepts manual inputs

**Requirements**:
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

**Validation Checklist**:
- [ ] Workflow appears in "Run workflow" dropdown
- [ ] All 3 inputs are available
- [ ] Inputs have correct types and defaults
- [ ] Workflow uses input values correctly
- [ ] Conditional logic works (force flag)
- [ ] Can be triggered manually from UI

---

### Task 12: Complete CI/CD Pipeline ⭐⭐⭐⭐⭐

**Objective**: Build a complete end-to-end pipeline

**Requirements**:
1. Create `.github/workflows/complete-pipeline.yml`
2. Pipeline stages:
   - **Lint**: Check code quality (create dummy lint script)
   - **Test**: Run tests (create dummy test script)
   - **Build**: Create build artifacts
   - **Security**: Run security scan
   - **Deploy Dev**: Auto-deploy to dev (on feature branches)
   - **Deploy Staging**: Auto-deploy to staging (on develop branch)
   - **Deploy Prod**: Manual approval for production (on master)
3. Use job dependencies correctly
4. Upload artifacts between stages
5. Add notifications (print deployment status)
6. Include rollback step (print rollback message if deploy fails)

**Validation Checklist**:
- [ ] All 6 stages exist and run in order
- [ ] Job dependencies are correct
- [ ] Artifacts are passed between jobs
- [ ] Conditional deployments work (branch-based)
- [ ] Production requires approval
- [ ] Rollback logic works
- [ ] Notifications are sent
- [ ] Pipeline completes end-to-end

---

## 🔴 Expert Tasks

### Task 13: Custom Composite Action ⭐⭐⭐⭐⭐

**Objective**: Create a reusable composite action

**Requirements**:
1. Create `.github/actions/setup-project/action.yml`:
   - Inputs: `language`, `version`, `install-command`
   - Sets up the specified language
   - Runs install command
   - Outputs: `setup-complete` (true/false)
2. Create `.github/workflows/use-composite-action.yml`:
   - Uses your composite action
   - Tests it with Python and Node.js
   - Uses the output to determine next steps

**Validation Checklist**:
- [ ] Composite action file structure is correct
- [ ] Action accepts inputs
- [ ] Action sets up environment correctly
- [ ] Action produces outputs
- [ ] Main workflow uses action successfully
- [ ] Outputs are accessible in main workflow

---

### Task 14: Dynamic Matrix Generation ⭐⭐⭐⭐⭐

**Objective**: Generate matrix dynamically based on file contents

**Requirements**:
1. Create a file `supported-versions.txt` with:
   ```
   python:3.9
   python:3.10
   python:3.11
   node:18
   node:20
   ```
2. Create `.github/workflows/dynamic-matrix.yml`:
   - Job 1: `generate-matrix`
     - Reads `supported-versions.txt`
     - Parses versions
     - Outputs matrix in JSON format
   - Job 2: `test-matrix`
     - Uses matrix from Job 1
     - Sets up correct language/version
     - Runs tests

**Validation Checklist**:
- [ ] Matrix is generated from file
- [ ] Matrix includes all versions from file
- [ ] Matrix format is correct JSON
- [ ] Test job uses dynamic matrix
- [ ] All matrix combinations run
- [ ] Adding new version to file creates new job

---

### Task 15: Self-Hosted Runner Setup (Optional) ⭐⭐⭐⭐⭐

**Objective**: Configure and use self-hosted runners

**Requirements**:
1. Set up a self-hosted runner (local machine or VM)
2. Create `.github/workflows/self-hosted.yml`:
   - Uses self-hosted runner
   - Labels: `self-hosted`, `linux` (or your OS)
   - Runs a test job
   - Uses runner-specific features (if any)

**Validation Checklist**:
- [ ] Runner is registered with GitHub
- [ ] Workflow uses self-hosted runner
- [ ] Runner labels are correct
- [ ] Job executes on self-hosted runner
- [ ] Runner appears in GitHub Settings

**Note**: This requires setting up a runner on your machine

---

## 📊 Progress Tracker

Track your progress here:

### Beginner Tasks
- [x] Task 1: Hello World Workflow ✅ (Validated - 95/100)
- [ ] Task 2: Multi-Step Job
- [ ] Task 3: Matrix Build - OS Testing
- [ ] Task 4: Conditional Steps

### Intermediate Tasks
- [ ] Task 5: Job Dependencies
- [ ] Task 6: Artifacts Upload/Download
- [ ] Task 7: Caching Dependencies
- [ ] Task 8: Matrix with Multiple Variables

### Advanced Tasks
- [ ] Task 9: Reusable Workflow
- [ ] Task 10: Environment Protection
- [ ] Task 11: Workflow Dispatch with Inputs
- [ ] Task 12: Complete CI/CD Pipeline

### Expert Tasks
- [ ] Task 13: Custom Composite Action
- [ ] Task 14: Dynamic Matrix Generation
- [ ] Task 15: Self-Hosted Runner Setup

---

## ✅ How Validation Works

1. **You complete the task** and create your workflow file
2. **Share the workflow file** with me
3. **I'll add inline comments** directly in your workflow file showing:
   - ✅ What you did well
   - ⚠️ What needs fixing
   - 📝 Suggestions for improvement
4. **I'll add a validation summary** at the bottom of your file with:
   - Checklist of requirements
   - Grade/Score
   - Status (Complete/Needs Fix)
5. **Update this progress tracker** when task is complete

**Benefits**:
- All feedback in one place (your workflow file)
- Easy to see what's good and what needs work
- Validation summary at bottom for quick reference
- Progress tracked here in this file

---

## 💡 Tips

- Start with beginner tasks and work your way up
- Test each workflow locally if possible (using `act`)
- Read error messages carefully
- Check GitHub Actions logs for debugging
- Don't hesitate to ask for hints!

---

## 🎯 Mastery Goals

- **Beginner Master**: Complete tasks 1-4
- **Intermediate Master**: Complete tasks 1-8
- **Advanced Master**: Complete tasks 1-12
- **Expert Master**: Complete all 15 tasks

---

**Ready to start? Pick a task and let's go! 🚀**

---

**Last Updated**: 2025
**Status**: Active Practice Tasks 📝

