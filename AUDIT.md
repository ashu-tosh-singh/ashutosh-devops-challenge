### 1. Issue: Kubernetes provider not configured properly

**File:** terraform/versions.tf

**Problem:**
Terraform was not using the correct Kubernetes context.

**Why it matters:**
Deployment failed because it tried to connect to the wrong cluster.

**Fix:**
Configured kubeconfig path and context explicitly.

### 2. Issue: setup.sh lacked error handling

**File:** setup.sh

**Problem:**
Script continued even if commands failed.

**Why it matters:**
Could lead to partial or broken setup.

**Fix:**
Added strict mode (`set -euo pipefail`).

### 3. Issue: setup.sh assumed correct Kubernetes context

**File:** setup.sh

**Problem:**
Script assumed correct cluster was already selected.

**Why it matters:**
Could deploy to wrong cluster.

**Fix:**
Added context validation.

### 4. Issue: setup.sh did not verify deployment

**File:** setup.sh

**Problem:**
Script did not check if deployment succeeded.

**Why it matters:**
False success even when app is not running.

**Fix:**
Added rollout status check.

### 5. Issue: Missing resource limits

**File:** helm/templates/deployment.yaml

**Problem:**
Deployment had no resource limits.

**Why it matters:**
Pods failed due to namespace quota.

**Fix:**
Added CPU and memory requests/limits.

### 6. Issue: Secret exposed in values.yaml

**File:** helm/values.yaml

**Problem:**
API token was stored in plaintext.

**Why it matters:**
Security risk — sensitive data exposed.

**Fix:**
Moved to Kubernetes Secret.

### 7. Issue: No metrics endpoint

**File:** app/main.py

**Problem:**
Application had no metrics.

**Why it matters:**
No visibility into traffic or performance.

**Fix:**
Added `/metrics` endpoint.

### 8. Issue: No request tracking

**File:** app/main.py

**Problem:**
Requests were not tracked.

**Why it matters:**
No insight into usage or latency.

**Fix:**
Added request count and latency metrics.

### 9. Issue: Metrics not discoverable

**File:** deployment.yaml

**Problem:**
Prometheus could not discover metrics.

**Why it matters:**
Metrics would not be collected.

**Fix:**
Added Prometheus annotations.

### 10. Issue: No policy enforcement

**Problem:**
No rules to prevent insecure deployments.

**Why it matters:**
Containers could run as root or without limits.

**Fix:**
Added Kyverno policies.

### 11. Issue: CI pipeline not enforcing validation

**Problem:**
Errors were ignored using `|| true`.

**Why it matters:**
Broken code could pass CI.

**Fix:**
Enabled strict validation and added security scan.

### 12. Issue: High number of vulnerabilities in Docker image

**File:** Docker image / CI pipeline

**Problem:**
Trivy scan detected many HIGH and CRITICAL vulnerabilities, mostly from base OS packages.

**Why it matters:**
These vulnerabilities can pose security risks in production environments.

**Fix:**
Added Trivy scan in CI for visibility and monitoring of vulnerabilities.