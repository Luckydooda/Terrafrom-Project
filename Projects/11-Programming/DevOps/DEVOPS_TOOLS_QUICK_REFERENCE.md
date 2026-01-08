# DevOps/SRE Tools Quick Reference Guide
## Topics to Study During Office Free Time

---

## 🔴 High Priority (You Need These!)

### 1. Nginx
**What:** Web server, reverse proxy, load balancer

**Key Concepts:**
- Reverse proxy configuration
- Load balancing (round-robin, least_conn, ip_hash)
- SSL/TLS termination
- Location blocks and routing
- Caching and compression

**Config Example:**
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Interview Questions:**
- What's the difference between proxy_pass and upstream?
- How do you configure SSL in Nginx?
- What's the difference between location / and location = /?

---

### 2. Helm
**What:** Kubernetes package manager

**Key Concepts:**
- Charts (packages)
- Values.yaml (configuration)
- Templates (Go templating)
- Releases (installed instances)
- Repositories

**Common Commands:**
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm search repo nginx
helm install my-nginx bitnami/nginx
helm upgrade my-nginx bitnami/nginx --set replicaCount=3
helm list
helm uninstall my-nginx
helm template my-chart ./my-chart  # Dry run
```

**Interview Questions:**
- What's the difference between `helm install` and `helm upgrade`?
- How do you pass custom values to a chart?
- What's a Helm release?

---

### 3. ArgoCD
**What:** GitOps continuous delivery tool for Kubernetes

**Key Concepts:**
- GitOps (Git as source of truth)
- Application CRDs
- Sync strategies (automatic/manual)
- Health status
- Rollback capabilities

**How It Works:**
```
1. Code pushed to Git
2. ArgoCD detects change
3. ArgoCD syncs K8s cluster with Git
4. K8s state = Git state
```

**Interview Questions:**
- What is GitOps?
- How does ArgoCD differ from Jenkins?
- What happens if someone manually changes K8s resources?

---

### 4. Trivy
**What:** Container security scanner

**Key Concepts:**
- Vulnerability scanning
- CVEs (Common Vulnerabilities and Exposures)
- Image scanning in CI/CD
- Severity levels (CRITICAL, HIGH, MEDIUM, LOW)

**Common Commands:**
```bash
# Scan an image
trivy image nginx:latest

# Scan with severity filter
trivy image --severity CRITICAL,HIGH nginx:latest

# Scan filesystem
trivy fs /path/to/project

# Scan Kubernetes
trivy k8s --report summary cluster
```

**Interview Questions:**
- At what stage should you run Trivy in CI/CD?
- What's a CVE?
- How do you handle critical vulnerabilities?

---

### 5. Service Mesh (Istio)
**What:** Infrastructure layer for service-to-service communication

**Key Concepts:**
- Sidecar proxy (Envoy)
- Traffic management (routing, retries, timeouts)
- Security (mTLS, authentication)
- Observability (metrics, tracing, logging)
- Service discovery

**Components:**
```
Istio Architecture:
├── Control Plane (istiod)
│   ├── Pilot (traffic management)
│   ├── Citadel (security)
│   └── Galley (configuration)
└── Data Plane (Envoy sidecars)
```

**Interview Questions:**
- What problem does a service mesh solve?
- What's a sidecar proxy?
- When should you NOT use a service mesh?

---

## 🟡 Medium Priority

### 6. Prometheus & PromQL
**Key Queries:**
```promql
# CPU usage by pod
sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)

# Memory usage
container_memory_usage_bytes

# HTTP request rate
rate(http_requests_total[5m])

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

### 7. Grafana
**Key Concepts:**
- Dashboards and panels
- Data sources (Prometheus, CloudWatch, etc.)
- Alerting rules
- Variables and templating
- Annotations

---

### 8. Vault (HashiCorp)
**What:** Secrets management

**Key Concepts:**
- Secrets engines
- Authentication methods
- Policies
- Dynamic secrets
- Encryption as a service

---

### 9. Fluentd / Fluent Bit
**What:** Log collection and forwarding

**Key Concepts:**
- Input plugins (tail, forward)
- Output plugins (elasticsearch, cloudwatch)
- Filters and parsers
- Buffer management

---

### 10. Kustomize
**What:** Kubernetes native configuration management

**Key Concepts:**
- Base and overlays
- Patches (strategic merge, JSON)
- ConfigMap/Secret generators
- Difference from Helm

---

## 📚 Quick Interview Questions Bank

### Kubernetes
1. What's the difference between Deployment and StatefulSet?
2. How does a Service discover pods?
3. What's the difference between ConfigMap and Secret?
4. Explain Kubernetes networking.
5. What happens when you run `kubectl apply`?

### Docker
1. What's the difference between CMD and ENTRYPOINT?
2. How do you reduce Docker image size?
3. What's a multi-stage build?
4. Difference between COPY and ADD?
5. What's a Docker layer?

### CI/CD
1. What's the difference between continuous delivery and deployment?
2. How do you implement blue-green deployment?
3. What's canary deployment?
4. How do you handle secrets in CI/CD?
5. What's the difference between Jenkins and ArgoCD?

### SRE Concepts
1. What are SLIs, SLOs, and SLAs?
2. What's an error budget?
3. How do you handle on-call incidents?
4. What's toil and how do you reduce it?
5. Explain the incident management process.

---

## 🔗 Quick Study Resources

| Topic | Resource |
|-------|----------|
| Nginx | [Nginx Docs](https://nginx.org/en/docs/) |
| Helm | [Helm Docs](https://helm.sh/docs/) |
| ArgoCD | [ArgoCD Docs](https://argo-cd.readthedocs.io/) |
| Istio | [Istio Docs](https://istio.io/latest/docs/) |
| Trivy | [Trivy Docs](https://aquasecurity.github.io/trivy/) |
| Prometheus | [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/) |
| SRE | [Google SRE Book](https://sre.google/sre-book/table-of-contents/) |

---

## 📝 Daily Study Plan (15-30 min)

| Day | Topic | Focus |
|-----|-------|-------|
| Mon | Nginx | Config, reverse proxy |
| Tue | Helm | Charts, values, commands |
| Wed | ArgoCD | GitOps, sync, concepts |
| Thu | Istio | Service mesh basics |
| Fri | Trivy | Scanning, CI/CD integration |
| Sat | PromQL | Query practice |
| Sun | Review | Interview questions |

---

*Last updated: January 8, 2026*
*Push to GitHub and review during office free time!*
