### 1. Decision: Explicitly set Kubernetes context

**Context:**
Terraform was connecting to the wrong Kubernetes cluster.

**Options considered:**
- Use default kubeconfig — simple but unreliable  
- Set context explicitly — reliable  

**Chosen:**
Set context explicitly  

**Rationale:**
Ensures Terraform always connects to the correct cluster  

**Cost / risk:**
Needs update if cluster changes  

### 2. Decision: Use strict bash mode in setup script

**Context:**
Script was not stopping on errors.

**Options considered:**
- Default bash behavior — ignores errors  
- Strict mode — fails immediately  

**Chosen:**
Strict mode (`set -euo pipefail`)  

**Rationale:**
Prevents partial or broken execution  

**Cost / risk:**
Script may fail more often  

### 3. Decision: Validate Kubernetes context in setup script

**Context:**
Deployment could go to the wrong cluster.

**Options considered:**
- Assume correct context — risky  
- Validate context — safer  

**Chosen:**
Validate context  

**Rationale:**
Avoids deploying to wrong cluster  

**Cost / risk:**
Adds small setup step  

### 4. Decision: Verify deployment using rollout status

**Context:**
No confirmation that deployment succeeded.

**Options considered:**
- Trust Helm output — not reliable  
- Check rollout status — reliable  

**Chosen:**
Check rollout status  

**Rationale:**
Ensures application is actually running  

**Cost / risk:**
Adds slight delay  

### 5. Decision: Define resource requests and limits

**Context:**
Pods failed due to namespace quota.

**Options considered:**
- No limits — simple but unreliable  
- Define limits — stable  

**Chosen:**
Define requests and limits  

**Rationale:**
Ensures pods can run properly  

**Cost / risk:**
Needs tuning  

### 6. Decision: Use Kubernetes Secret for API token

**Context:**
API token was exposed in values.yaml.

**Options considered:**
- Store in values.yaml — insecure  
- Use Kubernetes Secret — secure  
- Use external secret manager — more secure but complex  

**Chosen:**
Kubernetes Secret  

**Rationale:**
Improves security by removing plaintext secrets  

**Cost / risk:**
Secret stored in Terraform state  

### 7. Decision: Add /metrics endpoint

**Context:**
No visibility into application behavior.

**Options considered:**
- No metrics — no visibility  
- Add metrics — better monitoring  

**Chosen:**
Add /metrics  

**Rationale:**
Helps track requests and performance  

**Cost / risk:**
Adds small overhead  

### 8. Decision: Track request count and latency

**Context:**
Need to measure traffic and performance.

**Options considered:**
- No tracking — no insight  
- Track metrics — useful  

**Chosen:**
Track request count and latency  

**Rationale:**
Helps understand usage and response time  

**Cost / risk:**
Adds small complexity  

### 9. Decision: Use Prometheus annotations

**Context:**
Metrics must be collected automatically.

**Options considered:**
- Annotations — simple  
- ServiceMonitor — more complex  

**Chosen:**
Annotations  

**Rationale:**
Allows automatic metrics collection  

**Cost / risk:**
Less flexible than ServiceMonitor  

### 10. Decision: Use Kyverno for policy enforcement

**Context:**
No rules to prevent insecure deployments.

**Options considered:**
- No policies — risky  
- Kyverno — simple  
- Gatekeeper — more complex  

**Chosen:**
Kyverno  

**Rationale:**
Prevents insecure configurations like root containers  

**Cost / risk:**
Less flexible than Gatekeeper  

### 11. Decision: Enforce strict CI validation

**Context:**
CI pipeline was allowing errors to pass.

**Options considered:**
- Ignore errors — unsafe  
- Enforce validation — safe  

**Chosen:**
Strict validation  

**Rationale:**
Ensures only valid code and configs pass CI  

**Cost / risk:**
Pipeline may fail more often  