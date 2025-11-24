# 🚀 GitHub Actions Projects

This directory contains practical GitHub Actions workflows covering basic to advanced CI/CD scenarios.

## 📁 Project Structure

```
GitHub-Actions/
├── README.md                          # This file
├── workflows/
│   ├── 01-basic-ci.yml                # Basic CI workflow
│   ├── 02-docker-build-push.yml      # Docker build and push
│   ├── 03-multi-stage-pipeline.yml   # Build → Test → Deploy
│   ├── 04-matrix-builds.yml          # Matrix builds for multiple versions
│   ├── 05-environment-deployment.yml # Environment-based deployments
│   └── reusable/
│       ├── build-and-test.yml        # Reusable build workflow
│       └── deploy.yml                # Reusable deployment workflow
├── examples/
│   ├── python-app/                   # Sample Python application
│   ├── nodejs-app/                   # Sample Node.js application
│   └── docker-app/                   # Sample Docker application
└── docs/
    └── workflow-guide.md             # Detailed workflow documentation
```

## 🎯 Workflow Examples

### 1. Basic CI Workflow (`01-basic-ci.yml`)
- **Purpose**: Run tests on every push and pull request
- **Features**:
  - Automatic test execution
  - Multiple OS support (Ubuntu, Windows, macOS)
  - Test result reporting
  - Status badges

### 2. Docker Build & Push (`02-docker-build-push.yml`)
- **Purpose**: Build Docker images and push to container registry
- **Features**:
  - Multi-architecture builds (amd64, arm64)
  - Automated tagging
  - Push to Docker Hub / GitHub Container Registry
  - Cache optimization

### 3. Multi-Stage Pipeline (`03-multi-stage-pipeline.yml`)
- **Purpose**: Complete CI/CD pipeline with multiple stages
- **Features**:
  - Build stage
  - Test stage (unit, integration)
  - Security scanning
  - Deployment stage
  - Job dependencies and artifacts

### 4. Matrix Builds (`04-matrix-builds.yml`)
- **Purpose**: Test across multiple versions and environments
- **Features**:
  - Multiple Python/Node versions
  - Multiple OS combinations
  - Parallel execution
  - Conditional deployments

### 5. Environment Deployment (`05-environment-deployment.yml`)
- **Purpose**: Deploy to different environments with approval gates
- **Features**:
  - Environment protection rules
  - Manual approval for production
  - Environment-specific secrets
  - Rollback capability

### 6. Reusable Workflows (`reusable/`)
- **Purpose**: DRY principle - reusable workflow components
- **Features**:
  - Build and test workflow
  - Deployment workflow
  - Parameterized workflows
  - Workflow composition

## 🔧 Setup Instructions

### Prerequisites
1. GitHub repository with Actions enabled
2. Required secrets configured (see each workflow for details)

### Common Secrets to Configure
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password or token
- `AWS_ACCESS_KEY_ID` - AWS access key (for AWS deployments)
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `DEPLOY_TOKEN` - Deployment token

### Usage
1. Copy the workflow file to `.github/workflows/` in your repository
2. Customize the workflow for your project needs
3. Configure required secrets in repository settings
4. Push to trigger the workflow

## 📚 Learning Path

### Beginner
1. Start with `01-basic-ci.yml` - understand workflow structure
2. Modify it for your project's test commands
3. Add status badges to your README

### Intermediate
4. Implement `02-docker-build-push.yml` for containerized apps
5. Set up `03-multi-stage-pipeline.yml` for full CI/CD
6. Experiment with `04-matrix-builds.yml` for multi-version testing

### Advanced
7. Create environment-specific deployments with `05-environment-deployment.yml`
8. Build reusable workflows for organization-wide use
9. Implement custom actions for repeated tasks

## 🎓 Key Concepts Covered

- **Workflow Triggers**: `push`, `pull_request`, `schedule`, `workflow_dispatch`
- **Jobs and Steps**: Parallel and sequential execution
- **Secrets Management**: Secure credential handling
- **Artifacts**: Sharing files between jobs
- **Matrix Strategy**: Testing multiple configurations
- **Environment Protection**: Approval gates and secrets
- **Reusable Workflows**: DRY principle in CI/CD
- **Conditional Execution**: `if` conditions and expressions
- **Caching**: Speed up builds with dependency caching

## 🔍 Best Practices

1. **Security**
   - Never commit secrets to workflows
   - Use least-privilege IAM roles
   - Scan dependencies for vulnerabilities

2. **Performance**
   - Use caching for dependencies
   - Run jobs in parallel when possible
   - Optimize Docker layer caching

3. **Maintainability**
   - Use reusable workflows
   - Document workflow purpose
   - Version pin actions

4. **Reliability**
   - Add retry logic for flaky tests
   - Implement proper error handling
   - Use status checks for quality gates

## 📖 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

## 🚀 Next Steps

1. ✅ Set up basic CI workflow
2. ✅ Implement Docker builds
3. ✅ Create multi-stage pipeline
4. ⬜ Add security scanning
5. ⬜ Implement deployment automation
6. ⬜ Create reusable workflow library

---

**Last Updated**: 2025
**Status**: Active Development 🚀

