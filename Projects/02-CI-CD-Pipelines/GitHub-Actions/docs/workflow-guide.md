# GitHub Actions Workflow Guide

This guide provides detailed documentation for all GitHub Actions workflows in this repository.

## Table of Contents

1. [Basic CI Workflow](#1-basic-ci-workflow)
2. [Docker Build and Push](#2-docker-build-and-push)
3. [Multi-Stage Pipeline](#3-multi-stage-pipeline)
4. [Matrix Builds](#4-matrix-builds)
5. [Environment-Based Deployment](#5-environment-based-deployment)
6. [Reusable Workflows](#6-reusable-workflows)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## 1. Basic CI Workflow

**File**: `workflows/01-basic-ci.yml`

### Purpose
Runs automated tests on every push and pull request to ensure code quality.

### Features
- Multi-OS testing (Ubuntu, Windows, macOS)
- Multiple Python version support
- Code coverage reporting
- Security scanning with Trivy
- Test result artifacts

### Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

### Jobs

#### Test Job
- Runs on multiple OS and Python version combinations
- Installs dependencies
- Runs linter (flake8)
- Executes unit tests with coverage
- Uploads coverage reports to Codecov

#### Build Job
- Runs after tests pass
- Builds application package
- Uploads build artifacts

#### Security Job
- Scans codebase for vulnerabilities
- Uploads results to GitHub Security tab

### Setup Requirements
1. Create `requirements.txt` (or remove the step if not using Python)
2. Configure Codecov token (optional)
3. Ensure test files exist in `tests/` directory

### Customization
```yaml
# Modify Python versions
python-version: ['3.9', '3.10', '3.11']

# Add more test commands
- name: Run integration tests
  run: pytest tests/integration/
```

---

## 2. Docker Build and Push

**File**: `workflows/02-docker-build-push.yml`

### Purpose
Builds Docker images and pushes them to container registries with multi-platform support.

### Features
- Multi-architecture builds (amd64, arm64)
- Automated tagging based on branches/tags
- Vulnerability scanning
- SBOM (Software Bill of Materials) generation
- Build caching for faster builds

### Triggers
- Push to `main` or `develop`
- Version tags (e.g., `v1.0.0`)
- Pull requests (build only, no push)
- Manual dispatch with custom tag

### Jobs

#### Build and Push Job
- Sets up Docker Buildx for multi-platform builds
- Logs in to container registry
- Extracts metadata for intelligent tagging
- Builds and pushes images
- Scans images for vulnerabilities
- Generates SBOM

### Setup Requirements
1. **GitHub Container Registry** (default):
   - No additional setup needed
   - Uses `GITHUB_TOKEN` automatically

2. **Docker Hub**:
   - Set secrets: `DOCKER_USERNAME`, `DOCKER_PASSWORD`
   - Change `REGISTRY` env to `docker.io`

3. **Dockerfile**:
   - Ensure `Dockerfile` exists in repository root
   - Or specify custom context path

### Customization
```yaml
# Change registry
env:
  REGISTRY: docker.io  # or ghcr.io, quay.io, etc.

# Add build arguments
build-args: |
  BUILD_DATE=${{ github.event.head_commit.timestamp }}
  VCS_REF=${{ github.sha }}
  CUSTOM_ARG=value
```

### Tagging Strategy
- Branch names: `main`, `develop`
- Version tags: `v1.0.0`, `1.0.0`, `1.0`
- SHA: `main-abc123`
- Latest: Only on default branch

---

## 3. Multi-Stage Pipeline

**File**: `workflows/03-multi-stage-pipeline.yml`

### Purpose
Complete CI/CD pipeline with multiple stages: lint → test → build → security → deploy.

### Features
- Sequential job execution with dependencies
- Service containers (PostgreSQL, Redis)
- Integration testing
- Security scanning
- Environment-based deployments
- Deployment notifications

### Stages

1. **Lint and Format** - Code quality checks
2. **Unit Tests** - Fast feedback on code changes
3. **Integration Tests** - Test with real services
4. **Build** - Create deployable artifacts
5. **Security Scan** - Vulnerability detection
6. **Deploy Staging** - Automatic deployment to staging
7. **Deploy Production** - Production deployment with approval

### Setup Requirements

#### Services
- PostgreSQL: Configured automatically
- Redis: Configured automatically
- Add more services as needed

#### Secrets
- `SNYK_TOKEN` - For Snyk security scanning (optional)
- `STAGING_DEPLOY_TOKEN` - Staging deployment credentials
- `PRODUCTION_DEPLOY_TOKEN` - Production deployment credentials
- `SLACK_WEBHOOK_URL` - For notifications (optional)

#### Environment Configuration
Configure environments in GitHub repository settings:
- **Staging**: Add protection rules, secrets, reviewers
- **Production**: Require manual approval

### Customization
```yaml
# Add more services
services:
  mongodb:
    image: mongo:6
    ports:
      - 27017:27017

# Modify deployment commands
- name: Deploy to staging
  run: |
    aws s3 sync dist/ s3://staging-bucket/
    aws cloudfront create-invalidation --distribution-id $CF_ID --paths "/*"
```

---

## 4. Matrix Builds

**File**: `workflows/04-matrix-builds.yml`

### Purpose
Test applications across multiple versions, operating systems, and configurations simultaneously.

### Features
- Python version matrix (3.9-3.12)
- Node.js version matrix (18-22)
- Multi-platform Docker builds
- Database compatibility testing
- Parallel execution
- Build summary aggregation

### Matrix Strategies

#### Python Matrix
- Tests on Ubuntu, Windows, macOS
- Multiple Python versions
- Full test suite on specific combinations

#### Node.js Matrix
- Tests on multiple Node.js versions
- OS compatibility testing
- Coverage reporting for specific versions

#### Docker Matrix
- Multi-architecture builds (amd64, arm64, armv7)
- Platform-specific tagging

#### Database Matrix
- PostgreSQL 15, 16
- MySQL 8.0, 8.1
- MariaDB 11
- Automatic health checks

### Setup Requirements
1. **Python Projects**:
   - `requirements.txt` and `requirements-dev.txt`
   - Test files in `tests/` directory

2. **Node.js Projects**:
   - `package.json` with test scripts
   - Test files configured

3. **Docker Projects**:
   - `Dockerfile` in repository

4. **Database Projects**:
   - Database connection configuration
   - Test files that use database

### Customization
```yaml
# Add more versions
python-version: ['3.9', '3.10', '3.11', '3.12', '3.13']

# Exclude specific combinations
exclude:
  - os: windows-latest
    python-version: '3.9'

# Include specific combinations with extra config
include:
  - python-version: '3.11'
    os: ubuntu-latest
    test-suite: 'full'
    coverage: true
```

---

## 5. Environment-Based Deployment

**File**: `workflows/05-environment-deployment.yml`

### Purpose
Deploy to different environments (dev, staging, production) with appropriate gates and approvals.

### Features
- Automatic environment detection
- Manual approval for production
- Environment-specific secrets
- Pre-deployment validation
- Post-deployment monitoring
- Rollback capability
- Deployment notifications

### Environments

#### Development
- Automatic deployment from feature branches
- No approval required
- Fast feedback

#### Staging
- Automatic deployment from `develop` branch
- Integration and E2E tests
- Pre-production validation

#### Production
- Deployment from `main` branch
- Manual approval required (if configured)
- Backup creation
- Health checks
- Automatic rollback on failure
- GitHub release creation

### Setup Requirements

#### GitHub Environments
Configure in: Settings → Environments

1. **Development**:
   - URL: `https://dev.example.com`
   - Secrets: `DEV_DEPLOY_TOKEN`

2. **Staging**:
   - URL: `https://staging.example.com`
   - Secrets: `STAGING_DEPLOY_TOKEN`

3. **Production**:
   - URL: `https://example.com`
   - Secrets: `PRODUCTION_DEPLOY_TOKEN`
   - Protection rules: Required reviewers

#### AWS Credentials
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- IAM role with deployment permissions

#### Notifications
- `SLACK_WEBHOOK_URL` (optional)

### Customization
```yaml
# Add custom deployment commands
- name: Deploy to production
  run: |
    # Your deployment script
    ./scripts/deploy.sh production
    kubectl apply -f k8s/production/
    helm upgrade --install app ./helm-chart

# Add custom health checks
- name: Health check
  run: |
    for i in {1..10}; do
      if curl -f https://example.com/health; then
        echo "Health check passed"
        exit 0
      fi
      sleep 10
    done
    exit 1
```

---

## 6. Reusable Workflows

**Files**: 
- `workflows/reusable/build-and-test.yml`
- `workflows/reusable/deploy.yml`

### Purpose
DRY (Don't Repeat Yourself) principle - create reusable workflow components that can be called from multiple workflows.

### Build and Test Workflow

#### Inputs
- `node-version`: Node.js version
- `python-version`: Python version
- `install-command`: Dependency installation command
- `test-command`: Test execution command
- `build-command`: Build command
- `working-directory`: Working directory

#### Outputs
- `build-status`: Status of build job
- `test-status`: Status of test job

#### Usage
```yaml
jobs:
  build-and-test:
    uses: ./.github/workflows/reusable/build-and-test.yml
    with:
      node-version: '20'
      install-command: 'npm ci'
      test-command: 'npm test'
      build-command: 'npm run build'
```

### Deploy Workflow

#### Inputs
- `environment`: Target environment name
- `deployment-type`: Type (s3, kubernetes, ecs, lambda, cloudfront, docker)
- `artifact-name`: Artifact to deploy
- `aws-region`: AWS region
- `s3-bucket`: S3 bucket name
- `k8s-namespace`: Kubernetes namespace
- `k8s-manifest-path`: Path to K8s manifests
- `cloudfront-distribution-id`: CloudFront distribution ID

#### Secrets
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `DEPLOY_TOKEN`
- `KUBECONFIG`

#### Usage
```yaml
jobs:
  deploy:
    uses: ./.github/workflows/reusable/deploy.yml
    with:
      environment: production
      deployment-type: s3
      s3-bucket: my-bucket
      cloudfront-distribution-id: ${{ secrets.CF_ID }}
    secrets:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## Best Practices

### 1. Security
- ✅ Never commit secrets to workflows
- ✅ Use GitHub Secrets for sensitive data
- ✅ Use least-privilege IAM roles
- ✅ Scan dependencies regularly
- ✅ Pin action versions

### 2. Performance
- ✅ Use caching for dependencies
- ✅ Run jobs in parallel when possible
- ✅ Use matrix builds efficiently
- ✅ Optimize Docker layer caching
- ✅ Clean up old artifacts

### 3. Maintainability
- ✅ Use reusable workflows
- ✅ Document workflow purpose
- ✅ Version pin all actions
- ✅ Use descriptive job names
- ✅ Add comments for complex logic

### 4. Reliability
- ✅ Add retry logic for flaky tests
- ✅ Implement proper error handling
- ✅ Use status checks for quality gates
- ✅ Add health checks after deployment
- ✅ Implement rollback strategies

### 5. Cost Optimization
- ✅ Use self-hosted runners for large workloads
- ✅ Clean up old artifacts and logs
- ✅ Optimize workflow execution time
- ✅ Use conditional execution (`if` statements)

---

## Troubleshooting

### Common Issues

#### 1. Workflow Not Triggering
**Problem**: Workflow doesn't run on push/PR

**Solutions**:
- Check branch names match workflow triggers
- Ensure workflow file is in `.github/workflows/`
- Verify YAML syntax is valid
- Check repository Actions settings

#### 2. Permission Denied Errors
**Problem**: Workflow can't access resources

**Solutions**:
- Check repository permissions in workflow
- Verify secrets are configured correctly
- Ensure IAM roles have correct permissions
- Check environment protection rules

#### 3. Matrix Build Failures
**Problem**: Some matrix combinations fail

**Solutions**:
- Use `fail-fast: false` to see all results
- Check excluded combinations
- Verify all versions are supported
- Review platform-specific issues

#### 4. Slow Workflow Execution
**Problem**: Workflows take too long

**Solutions**:
- Enable dependency caching
- Use Docker layer caching
- Run jobs in parallel
- Optimize test execution
- Consider self-hosted runners

#### 5. Deployment Failures
**Problem**: Deployment doesn't work

**Solutions**:
- Verify deployment credentials
- Check environment configuration
- Review deployment logs
- Test deployment commands locally
- Verify network connectivity

### Debugging Tips

1. **Enable Debug Logging**:
   ```yaml
   env:
     ACTIONS_STEP_DEBUG: true
     ACTIONS_RUNNER_DEBUG: true
   ```

2. **Check Workflow Logs**:
   - Go to Actions tab
   - Click on failed workflow run
   - Review job and step logs

3. **Test Locally**:
   - Use `act` tool to run workflows locally
   - Test deployment scripts manually
   - Verify environment setup

4. **Use Artifacts**:
   - Upload debug information as artifacts
   - Download and inspect build outputs
   - Check test result files

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Best Practices for GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/best-practices)
- [Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

---

**Last Updated**: 2025
**Maintained By**: DevOps Team

