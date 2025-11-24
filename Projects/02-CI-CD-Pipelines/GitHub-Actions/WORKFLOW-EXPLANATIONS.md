# 📚 Complete Guide to GitHub Actions Workflows

This document explains the purpose and functionality of each GitHub Actions workflow file.

---

## 📋 Table of Contents

1. [01-basic-ci.yml - Basic CI Workflow](#1-01-basic-ciyml---basic-ci-workflow)
2. [02-docker-build-push.yml - Docker Build and Push](#2-02-docker-build-pushyml---docker-build-and-push)
3. [03-multi-stage-pipeline.yml - Multi-Stage CI/CD Pipeline](#3-03-multi-stage-pipelineyml---multi-stage-cicd-pipeline)
4. [04-matrix-builds.yml - Matrix Builds](#4-04-matrix-buildsyml---matrix-builds)
5. [05-environment-deployment.yml - Environment-Based Deployment](#5-05-environment-deploymentyml---environment-based-deployment)
6. [06-using-reusable-workflows.yml - Using Reusable Workflows](#6-06-using-reusable-workflowsyml---using-reusable-workflows)
7. [Reusable Workflows](#7-reusable-workflows)

---

## 1. `01-basic-ci.yml` - Basic CI Workflow

### 🎯 Purpose
**Basic Continuous Integration workflow** - Runs automated tests and checks on every code change.

### 🔄 When It Runs
- ✅ Push to `main`, `master`, or `develop` branches
- ✅ Pull requests to `main`, `master`, or `develop`
- ✅ Manual trigger via workflow_dispatch

### 📦 What It Does

#### Job 1: Test (`test`)
- **Multi-OS Testing**: Runs on Ubuntu, Windows, and macOS
- **Multi-Version Testing**: Tests with Python 3.9, 3.10, and 3.11
- **Steps**:
  1. Checks out your code
  2. Sets up Python environment
  3. Installs dependencies from `requirements.txt`
  4. Runs code linter (flake8) to check code quality
  5. Runs unit tests with pytest
  6. Generates code coverage reports
  7. Uploads test results and coverage to artifacts

#### Job 2: Build (`build`)
- **Runs After**: Test job completes successfully
- **Steps**:
  1. Checks out code
  2. Sets up Python
  3. Builds Python package (creates distribution files)
  4. Uploads build artifacts (`.tar.gz`, `.whl` files)

#### Job 3: Security Scan (`security`)
- **Runs In Parallel**: Doesn't wait for other jobs
- **Steps**:
  1. Scans codebase for vulnerabilities using Trivy
  2. Uploads security findings to GitHub Security tab

### 💡 Use Cases
- ✅ Quick feedback on code changes
- ✅ Ensure code works on multiple platforms
- ✅ Catch bugs before merging
- ✅ Track code coverage over time

### 🔧 Key Features
- Matrix strategy for multiple OS/versions
- Artifact uploads for test results
- Security scanning
- Code coverage tracking

---

## 2. `02-docker-build-push.yml` - Docker Build and Push

### 🎯 Purpose
**Builds Docker container images** and pushes them to container registries (GitHub Container Registry or Docker Hub).

### 🔄 When It Runs
- ✅ Push to `main` or `develop` branches
- ✅ Version tags (e.g., `v1.0.0`, `v2.3.1`)
- ✅ Pull requests (builds but doesn't push)
- ✅ Manual trigger with custom image tag

### 📦 What It Does

#### Job: Build and Push (`build-and-push`)
- **Multi-Platform Builds**: Creates images for `linux/amd64` and `linux/arm64`
- **Steps**:
  1. Checks out code
  2. Sets up Docker Buildx (for multi-platform builds)
  3. Logs in to container registry (GitHub Container Registry by default)
  4. Extracts metadata for intelligent tagging:
     - Branch names: `main`, `develop`
     - Version tags: `v1.0.0`, `1.0.0`, `1.0`
     - Commit SHA: `main-abc123`
     - Latest tag for default branch
  5. Builds Docker image with caching for speed
  6. Pushes image to registry
  7. Scans image for vulnerabilities (Trivy)
  8. Generates SBOM (Software Bill of Materials) - lists all dependencies

### 💡 Use Cases
- ✅ Containerize applications
- ✅ Deploy to Kubernetes, Docker Swarm, or cloud platforms
- ✅ Create multi-architecture images (works on Intel and ARM)
- ✅ Version control for container images

### 🔧 Key Features
- Multi-architecture support (AMD64, ARM64)
- Intelligent tagging based on branches/tags
- Image vulnerability scanning
- SBOM generation for security compliance
- Build caching for faster builds

### 📝 Requirements
- `Dockerfile` in repository root
- Container registry credentials (if using Docker Hub)

---

## 3. `03-multi-stage-pipeline.yml` - Multi-Stage CI/CD Pipeline

### 🎯 Purpose
**Complete end-to-end CI/CD pipeline** with multiple stages: Lint → Test → Build → Security → Deploy.

### 🔄 When It Runs
- ✅ Push to `main` or `develop`
- ✅ Pull requests to `main`
- ✅ Release publication
- ✅ Manual trigger

### 📦 What It Does

#### Stage 1: Lint and Format (`lint-and-format`)
- Checks code quality and formatting
- Runs ESLint and format checks
- Uploads lint results

#### Stage 2: Unit Tests (`unit-tests`)
- **Runs After**: Lint stage
- Tests on multiple OS (Ubuntu, Windows, macOS)
- Tests with multiple Node.js versions (18, 20, 21)
- Generates coverage reports
- Uploads test results

#### Stage 3: Integration Tests (`integration-tests`)
- **Runs After**: Unit tests pass
- **Services**: Sets up PostgreSQL and Redis containers
- Tests application with real database and cache
- Validates integration between components

#### Stage 4: Build (`build`)
- **Runs After**: Integration tests pass
- Builds application for production
- Creates release packages (`.tar.gz`, `.zip`)
- Uploads build artifacts

#### Stage 5: Security Scan (`security-scan`)
- **Runs After**: Build completes
- Runs npm audit for dependency vulnerabilities
- Runs Snyk security scan
- Runs Trivy filesystem scan
- Uploads security findings

#### Stage 6: Deploy to Staging (`deploy-staging`)
- **Runs After**: Build and security pass
- **Only On**: `develop` branch
- Deploys to staging environment
- Runs smoke tests to verify deployment

#### Stage 7: Deploy to Production (`deploy-production`)
- **Runs After**: Build and security pass
- **Only On**: `main` branch or release
- **Requires**: Manual approval (if configured)
- Creates backup before deployment
- Deploys to production
- Runs smoke tests
- Performs health checks
- Creates GitHub release
- Sends notifications

### 💡 Use Cases
- ✅ Full software delivery pipeline
- ✅ Quality gates before deployment
- ✅ Automated testing at multiple levels
- ✅ Production-ready deployments

### 🔧 Key Features
- Sequential job execution with dependencies
- Service containers for integration testing
- Environment-based deployments
- Manual approval gates
- Rollback capability
- Deployment notifications

---

## 4. `04-matrix-builds.yml` - Matrix Builds

### 🎯 Purpose
**Test applications across multiple versions, operating systems, and configurations** simultaneously using matrix strategy.

### 🔄 When It Runs
- ✅ Push to `main` or `develop`
- ✅ Pull requests to `main`
- ✅ Manual trigger

### 📦 What It Does

#### Job 1: Python Matrix (`python-matrix`)
- Tests Python code on:
  - **Versions**: 3.9, 3.10, 3.11, 3.12
  - **OS**: Ubuntu, Windows, macOS
  - **Total**: ~12 combinations
- Runs full test suite on specific combinations
- Uploads coverage for selected versions

#### Job 2: Node.js Matrix (`nodejs-matrix`)
- Tests Node.js code on:
  - **Versions**: 18, 20, 21, 22
  - **OS**: Ubuntu, Windows, macOS
- Runs tests and coverage

#### Job 3: Docker Matrix (`docker-matrix`)
- Builds Docker images for:
  - **Platforms**: `linux/amd64`, `linux/arm64`, `linux/arm/v7`
- Tests multi-architecture support
- Creates platform-specific tags

#### Job 4: Database Matrix (`database-matrix`)
- Tests application with different databases:
  - **PostgreSQL**: 15, 16
  - **MySQL**: 8.0, 8.1
  - **MariaDB**: 11
- Validates database compatibility
- Tests migrations and queries

#### Job 5: Build Summary (`build-summary`)
- Aggregates results from all matrix jobs
- Creates summary report
- Fails if any matrix job failed

### 💡 Use Cases
- ✅ Ensure compatibility across versions
- ✅ Test on multiple platforms
- ✅ Validate database migrations work on all DBs
- ✅ Build multi-architecture Docker images

### 🔧 Key Features
- Parallel execution (all combinations run simultaneously)
- `fail-fast: false` - continues even if one fails
- Include/exclude specific combinations
- Summary aggregation

---

## 5. `05-environment-deployment.yml` - Environment-Based Deployment

### 🎯 Purpose
**Deploy to different environments** (development, staging, production) with appropriate gates, approvals, and safety checks.

### 🔄 When It Runs
- ✅ Push to `main`, `develop`, or `feature/*` branches
- ✅ Pull requests to `main`
- ✅ Manual trigger with environment selection

### 📦 What It Does

#### Job 1: Pre-Deployment (`pre-deployment`)
- Validates deployment configuration
- Determines target environment based on branch:
  - `main` → production
  - `develop` → staging
  - `feature/*` → development
- Checks branch protection rules

#### Job 2: Build and Test (`build-and-test`)
- **Runs Before**: Any deployment
- **Skips If**: `force_deploy` is enabled
- Builds application
- Runs all tests
- Creates build artifacts

#### Job 3: Deploy to Development (`deploy-development`)
- **Runs On**: Feature branches or manual selection
- **No Approval Required**
- Deploys to development environment
- Runs smoke tests
- Sends notifications

#### Job 4: Deploy to Staging (`deploy-staging`)
- **Runs On**: `develop` branch
- **No Approval Required** (but can be configured)
- Deploys to staging environment
- Runs integration tests
- Runs end-to-end (E2E) tests
- Sends notifications

#### Job 5: Deploy to Production (`deploy-production`)
- **Runs On**: `main` branch or release
- **Requires**: Manual approval (if configured in GitHub)
- **Safety Features**:
  - Creates backup before deployment
  - Deploys to production
  - Runs smoke tests
  - Performs health checks
  - Automatic rollback on failure
  - Creates GitHub release
  - Sends notifications

#### Job 6: Post-Deployment Monitoring (`post-deployment-monitoring`)
- Monitors deployment health
- Generates deployment report
- Tracks metrics and error rates

### 💡 Use Cases
- ✅ Separate environments for dev/staging/prod
- ✅ Controlled production deployments
- ✅ Automatic deployments to dev/staging
- ✅ Safety checks and rollbacks

### 🔧 Key Features
- Environment protection rules
- Manual approval gates
- Automatic rollback
- Health checks
- Deployment notifications
- Backup creation

### 📝 Requirements
- Configure environments in GitHub Settings
- Set up environment-specific secrets
- Configure deployment targets (AWS, Kubernetes, etc.)

---

## 6. `06-using-reusable-workflows.yml` - Using Reusable Workflows

### 🎯 Purpose
**Example workflow** showing how to use reusable workflows to avoid code duplication.

### 🔄 When It Runs
- ✅ Push to `main` or `develop`
- ✅ Pull requests to `main`
- ✅ Manual trigger

### 📦 What It Does

#### Job 1: Build and Test
- **Calls**: `reusable/build-and-test.yml`
- Passes parameters:
  - Node.js version
  - Python version
  - Install command
  - Test command
  - Build command
- Gets back: Build and test status

#### Job 2: Deploy to Staging
- **Calls**: `reusable/deploy.yml`
- **Only On**: `develop` branch
- Passes deployment parameters
- Deploys to S3 bucket
- Invalidates CloudFront cache

#### Job 3: Deploy to Production
- **Calls**: `reusable/deploy.yml`
- **Only On**: `main` branch
- Deploys to Kubernetes
- Uses production namespace

### 💡 Use Cases
- ✅ Reuse common workflows across projects
- ✅ Maintain consistency
- ✅ Reduce code duplication
- ✅ Centralize workflow logic

### 🔧 Key Features
- Workflow composition
- Parameter passing
- Conditional execution
- Secret management

---

## 7. Reusable Workflows

### 📁 Location
`.github/workflows/reusable/`

### 📄 Files

#### `build-and-test.yml`
**Purpose**: Reusable workflow for building and testing applications

**Inputs**:
- `node-version`: Node.js version
- `python-version`: Python version
- `install-command`: Command to install dependencies
- `test-command`: Command to run tests
- `build-command`: Command to build
- `working-directory`: Working directory path

**Outputs**:
- `build-status`: Status of build job
- `test-status`: Status of test job

**Usage**: Call from other workflows to standardize build/test process

---

#### `deploy.yml`
**Purpose**: Reusable workflow for deploying to various platforms

**Inputs**:
- `environment`: Target environment name
- `deployment-type`: Type (s3, kubernetes, ecs, lambda, cloudfront, docker)
- `artifact-name`: Name of artifact to deploy
- `aws-region`: AWS region
- `s3-bucket`: S3 bucket name
- `k8s-namespace`: Kubernetes namespace
- `k8s-manifest-path`: Path to K8s manifests
- `cloudfront-distribution-id`: CloudFront distribution ID

**Secrets**:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `DEPLOY_TOKEN`
- `KUBECONFIG`

**Usage**: Call from other workflows to deploy to different platforms

---

## 🎓 Learning Path

### Beginner
1. Start with `01-basic-ci.yml` - understand workflow structure
2. Modify it for your project's needs
3. See tests run automatically

### Intermediate
4. Use `02-docker-build-push.yml` for containerized apps
5. Implement `03-multi-stage-pipeline.yml` for full CI/CD
6. Experiment with `04-matrix-builds.yml` for multi-version testing

### Advanced
7. Set up `05-environment-deployment.yml` for production deployments
8. Create reusable workflows for organization-wide use
9. Customize workflows for your specific needs

---

## 🔑 Key Concepts

### Workflow Triggers
- `push`: Runs on code push
- `pull_request`: Runs on PR creation/update
- `workflow_dispatch`: Manual trigger
- `schedule`: Cron-based scheduling
- `release`: On release publication

### Jobs
- Run in parallel by default
- Use `needs:` to create dependencies
- Can have conditions with `if:`

### Steps
- Sequential execution within a job
- Can use actions from marketplace
- Can run shell commands
- Can upload/download artifacts

### Matrix Strategy
- Run same job with different configurations
- Test multiple versions/platforms
- Parallel execution

### Environments
- Separate configurations per environment
- Protection rules (approvals, secrets)
- Environment-specific secrets

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

---

**Last Updated**: 2025
**Status**: Active Learning Project 🚀

