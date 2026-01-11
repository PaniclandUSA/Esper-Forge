# ESPER-FORGE: Deployment Guide

## Purpose of This Document

This document provides **practical guidance for deploying ESPER-FORGE** in production environments, including:
- Infrastructure requirements
- Integration patterns
- Operational considerations
- Security hardening
- Monitoring and maintenance
- Scaling strategies

This is an **illustrative document** (see [docs/README.md](README.md) for taxonomy).

For system architecture, see [04-ARCHITECTURE.md](04-ARCHITECTURE.md).

For specific applications, see [05-LITERACY-DEMO.md](05-LITERACY-DEMO.md), [06-JOURNALISM-DEMO.md](06-JOURNALISM-DEMO.md), [07-LEGAL-STANDARD.md](07-LEGAL-STANDARD.md).

---

## Deployment Scenarios

### Scenario 1: Literacy Organization (Self-Hosted)

**Profile**:
- 500-5,000 learners
- Weekly narrative processing (not real-time)
- Volunteer tutors with tablets
- Community-based deployment

**Infrastructure**:
```
Single server or cloud VM:
- 8 CPU cores
- 32 GB RAM
- 500 GB SSD storage
- Ubuntu 24.04 LTS

Estimated cost: $150-300/month (cloud) or $2,000 one-time (self-hosted)
```

**Stack**:
```
┌─────────────────────────────────────┐
│  Web Interface (Tutor Portal)      │
│  - Story submission                 │
│  - Progress tracking                │
│  - Certificate viewing              │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  ESPER-FORGE API Server             │
│  - REST endpoints                   │
│  - Background processing queue      │
│  - Certificate generation           │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  PostgreSQL Database                │
│  - Learner records                  │
│  - Story versions                   │
│  - Certificates                     │
│  - Audit logs                       │
└─────────────────────────────────────┘
```

---

### Scenario 2: News Organization (Cloud-Native)

**Profile**:
- 50-200 investigations/year
- High-stakes contested events
- Need for rapid certification
- Multiple reporters/editors

**Infrastructure**:
```
Cloud architecture (AWS/GCP/Azure):
- Application tier: 4-8 instances (auto-scaling)
- Processing tier: Compute cluster (16+ cores per job)
- Database: Managed PostgreSQL (replication)
- Storage: S3/Cloud Storage for artifacts
- CDN: Certificate delivery
```

**Estimated cost**: $2,000-5,000/month

**Stack**:
```
┌──────────────────────────────────────────┐
│  Load Balancer + WAF                     │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│  Application Servers (Auto-scaled)       │
│  - REST API                              │
│  - WebSocket (real-time status)          │
│  - Authentication (OAuth2)               │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│  Message Queue (RabbitMQ/SQS)            │
│  - Async job processing                  │
│  - Priority queuing                      │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│  Worker Pool (Horizontal scaling)        │
│  - ESPER-FORGE operators                 │
│  - VSE compilation                       │
│  - Certificate generation                │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│  Data Layer                              │
│  - PostgreSQL (metadata)                 │
│  - Object storage (artifacts)            │
│  - Certificate registry (blockchain)     │
└──────────────────────────────────────────┘
```

---

### Scenario 3: Legal System Integration (Enterprise)

**Profile**:
- Court system adoption
- High security requirements
- Compliance (SOC2, FedRAMP)
- Multi-tenant (multiple jurisdictions)

**Infrastructure**:
```
On-premises or private cloud:
- High availability (99.99% uptime)
- Disaster recovery (multi-region)
- Hardware Security Module (HSM) for signing
- Air-gapped certificate registry
- Audit logging to SIEM
```

**Estimated cost**: $50,000-200,000/year (includes compliance)

**Stack**:
```
┌──────────────────────────────────────────┐
│  API Gateway + mTLS                      │
│  - Certificate-based authentication      │
│  - Rate limiting per jurisdiction        │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│  Application Cluster (HA)                │
│  - Active-active across zones            │
│  - Session replication                   │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│  HSM Integration                         │
│  - Private key never leaves HSM          │
│  - FIPS 140-2 Level 3 compliant          │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│  Database Cluster (Multi-master)         │
│  - Synchronous replication               │
│  - Point-in-time recovery                │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│  Blockchain Certificate Registry         │
│  - Immutable audit trail                 │
│  - Public verification endpoint          │
└──────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

**System requirements**:
```
- Linux (Ubuntu 24.04 LTS recommended)
- Python 3.11+
- PostgreSQL 15+
- Redis 7+ (for caching and queues)
- 16 GB RAM minimum (32 GB recommended)
- 4 CPU cores minimum (8 cores recommended)
```

**Dependencies**:
```bash
# System packages
apt-get update
apt-get install -y \
    python3.11 \
    python3.11-dev \
    postgresql-15 \
    postgresql-contrib-15 \
    redis-server \
    nginx \
    certbot \
    build-essential \
    git

# Python packages (requirements.txt)
esper-vse>=1.1.0
esper-chronocore>=1.1.0
esper-pivotgram>=1.1.0
esper-pictogram>=1.1.0
numpy>=1.24.0
scipy>=1.11.0
cryptography>=41.0.0
pydantic>=2.0.0
fastapi>=0.104.0
sqlalchemy>=2.0.0
alembic>=1.12.0
celery>=5.3.0
redis>=5.0.0
```

---

### Quick Start (Development)
```bash
# 1. Clone repository
git clone https://github.com/PaniclandUSA/Esper-Forge.git
cd Esper-Forge

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Initialize database
createdb esper_forge
alembic upgrade head

# 5. Generate keypair (dev only - use HSM in production)
python -m esper_forge.crypto.keygen --output keys/

# 6. Configure
cp config.example.yml config.yml
# Edit config.yml with your settings

# 7. Start services
# Terminal 1: Redis
redis-server

# Terminal 2: Celery worker
celery -A esper_forge.tasks worker --loglevel=info

# Terminal 3: API server
uvicorn esper_forge.api:app --reload

# 8. Verify
curl http://localhost:8000/health
# Should return: {"status": "healthy", "version": "1.1.0"}
```

---

### Production Installation
```bash
# 1. Provision infrastructure
# (Use Terraform/CloudFormation - see /infrastructure directory)

# 2. Secure configuration
cat > /etc/esper-forge/config.yml <<EOF
database:
  url: postgresql://esper:PASSWORD@db.internal:5432/esper_forge
  pool_size: 20
  max_overflow: 10

redis:
  url: redis://redis.internal:6379/0

security:
  private_key_path: /dev/hsm0  # HSM device
  certificate_registry: https://certs.esper-forge.org
  api_keys_required: true

processing:
  worker_count: 16
  max_concurrent_jobs: 100
  timeout_seconds: 3600

logging:
  level: INFO
  syslog: true
  siem_endpoint: https://siem.internal/events
EOF

# 3. Set up service
cat > /etc/systemd/system/esper-forge-api.service <<EOF
[Unit]
Description=ESPER-FORGE API Server
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=esper-forge
Group=esper-forge
WorkingDirectory=/opt/esper-forge
ExecStart=/opt/esper-forge/venv/bin/gunicorn \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile /var/log/esper-forge/access.log \
    --error-logfile /var/log/esper-forge/error.log \
    esper_forge.api:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 4. Set up worker
cat > /etc/systemd/system/esper-forge-worker@.service <<EOF
[Unit]
Description=ESPER-FORGE Worker %i
After=network.target redis.service

[Service]
Type=simple
User=esper-forge
Group=esper-forge
WorkingDirectory=/opt/esper-forge
ExecStart=/opt/esper-forge/venv/bin/celery \
    -A esper_forge.tasks \
    worker \
    --loglevel=info \
    --concurrency=2 \
    --max-tasks-per-child=100
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 5. Enable and start
systemctl daemon-reload
systemctl enable esper-forge-api
systemctl enable esper-forge-worker@{1..8}
systemctl start esper-forge-api
systemctl start esper-forge-worker@{1..8}

# 6. Configure nginx reverse proxy
cat > /etc/nginx/sites-available/esper-forge <<EOF
upstream esper_forge {
    server 127.0.0.1:8000;
}

server {
    listen 443 ssl http2;
    server_name api.esper-forge.org;

    ssl_certificate /etc/letsencrypt/live/api.esper-forge.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.esper-forge.org/privkey.pem;

    location / {
        proxy_pass http://esper_forge;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts for long-running certifications
        proxy_read_timeout 3600s;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
    }
}
EOF

ln -s /etc/nginx/sites-available/esper-forge /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

---

## API Usage

### Authentication

**API keys required for production**:
```bash
# Generate API key (admin operation)
esper-forge-admin create-api-key \
    --org "Metropolitan Daily News" \
    --rate-limit 100/hour \
    --scopes certification,verification

# Returns:
# API Key: ef_live_7a3f9b2e8c1d4f5a6b7c8d9e0f1a2b3c
# Secret: sk_live_1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d
```

**Using API key**:
```bash
curl -X POST https://api.esper-forge.org/v1/certify \
    -H "Authorization: Bearer ef_live_7a3f9b2e8c1d4f5a6b7c8d9e0f1a2b3c" \
    -H "Content-Type: application/json" \
    -d @request.json
```

---

### Endpoints

#### POST /v1/certify

**Request**:
```json
{
  "artifact_type": "literacy_narrative",
  "source": {
    "type": "audio",
    "url": "https://storage.example.com/learner_story.wav",
    "metadata": {
      "learner_id": "anonymized_hash",
      "recording_date": "2026-01-10",
      "duration_seconds": 187
    }
  },
  "contract": {
    "semantic_invariants": [
      "emotional_core_preservation",
      "agency_attribution"
    ],
    "material_constraints": [
      "identity_privacy",
      "cultural_authenticity"
    ],
    "temporal_bounds": {
      "causality": "acyclic",
      "temporal_coherence_threshold": 0.05
    },
    "ethical_axioms": [
      "zero_shame_guarantee",
      "human_collapse_only"
    ]
  },
  "outputs_requested": [
    "grade_1",
    "grade_5",
    "grade_12"
  ]
}
```

**Response** (202 Accepted):
```json
{
  "job_id": "job_3f7a8b2c9d4e1f5a",
  "status": "processing",
  "estimated_completion": "2026-01-10T18:30:00Z",
  "status_url": "https://api.esper-forge.org/v1/jobs/job_3f7a8b2c9d4e1f5a"
}
```

---

#### GET /v1/jobs/{job_id}

**Response** (while processing):
```json
{
  "job_id": "job_3f7a8b2c9d4e1f5a",
  "status": "processing",
  "progress": 0.65,
  "current_stage": "Layer 4: Conservation Validation",
  "started_at": "2026-01-10T18:00:00Z",
  "estimated_completion": "2026-01-10T18:30:00Z"
}
```

**Response** (completed):
```json
{
  "job_id": "job_3f7a8b2c9d4e1f5a",
  "status": "completed",
  "certificate": {
    "url": "https://certs.esper-forge.org/cert_4f8a2b9c.json",
    "hash": "0x4f8a2b9c3e7d6f1a5b8c2e9f3a6d4b7c1e8f9a2d5b",
    "signature": "0x...",
    "public_key": "0x..."
  },
  "outputs": {
    "grade_1": "https://storage.example.com/output/grade_1.txt",
    "grade_5": "https://storage.example.com/output/grade_5.txt",
    "grade_12": "https://storage.example.com/output/grade_12.txt"
  },
  "completed_at": "2026-01-10T18:25:33Z"
}
```

---

#### POST /v1/verify

**Request**:
```json
{
  "certificate_url": "https://certs.esper-forge.org/cert_4f8a2b9c.json",
  "artifact_url": "https://storage.example.com/output/grade_12.txt"
}
```

**Response**:
```json
{
  "valid": true,
  "checks": {
    "signature_valid": true,
    "certificate_in_registry": true,
    "artifact_matches_hash": true,
    "timestamp_valid": true
  },
  "certificate_data": {
    "artifact_type": "literacy_narrative",
    "conservation_status": "PRESERVED",
    "dignity_violations": 0,
    "issued_at": "2026-01-10T18:25:33Z"
  }
}
```

---

## Integration Patterns

### Pattern 1: Asynchronous Batch Processing

**Use case**: Literacy organization processes stories overnight
```python
from esper_forge import ForgeClient

client = ForgeClient(
    api_key="ef_live_...",
    base_url="https://api.esper-forge.org"
)

# Submit batch
jobs = []
for story in learner_stories:
    job = client.certify_async(
        artifact_type="literacy_narrative",
        source=story.audio_file,
        contract=standard_literacy_contract
    )
    jobs.append(job)

# Wait for completion (with progress tracking)
results = client.wait_for_jobs(
    jobs,
    timeout=3600,  # 1 hour
    callback=lambda job: print(f"Progress: {job.progress}")
)

# Process results
for result in results:
    if result.status == "completed":
        save_certificate(result.certificate)
        notify_tutor(result.learner_id, result.outputs)
    else:
        handle_error(result.error)
```

---

### Pattern 2: Real-Time Streaming

**Use case**: News organization gets real-time status during investigation
```python
import asyncio
from esper_forge import ForgeStreamingClient

client = ForgeStreamingClient(
    api_key="ef_live_...",
    websocket_url="wss://api.esper-forge.org/v1/stream"
)

async def certify_investigation(witnesses):
    job = await client.certify_streaming(
        artifact_type="journalistic_investigation",
        witnesses=witnesses,
        contract=journalism_contract
    )
    
    async for update in job.stream():
        print(f"Stage: {update.stage}")
        print(f"Progress: {update.progress}")
        
        if update.stage == "decoherence_analysis":
            # Show reporter preliminary findings
            show_decoherence_preview(update.partial_results)
    
    certificate = await job.result()
    return certificate

# Run
asyncio.run(certify_investigation(witness_interviews))
```

---

### Pattern 3: Embedded Validation

**Use case**: Content management system validates on publish
```python
from esper_forge import ForgeValidator

# Initialize validator with cached keys
validator = ForgeValidator(
    public_key_url="https://api.esper-forge.org/v1/public-key",
    cache_ttl=3600
)

def publish_article(article, certificate_url):
    # Verify certificate before publishing
    is_valid, details = validator.verify(
        certificate_url=certificate_url,
        artifact=article.content
    )
    
    if not is_valid:
        raise PublishError(f"Certificate invalid: {details.error}")
    
    # Embed certificate link
    article.metadata["esper_forge_certificate"] = certificate_url
    article.metadata["verification_timestamp"] = now()
    
    # Publish with certificate badge
    article.publish(show_certificate_badge=True)
```

---

## Security Hardening

### Private Key Management

**Development** (NOT for production):
```bash
# Generate keypair locally
python -m esper_forge.crypto.keygen \
    --algorithm ed25519 \
    --output keys/

# Keys stored in files (insecure)
```

**Production** (required):
```bash
# Use Hardware Security Module (HSM)
# - AWS CloudHSM
# - Azure Dedicated HSM
# - On-premises HSM (Thales, Gemalto)

# Configure ESPER-FORGE to use HSM
cat > /etc/esper-forge/hsm.yml <<EOF
hsm:
  type: aws_cloudhsm
  cluster_id: cluster-xyz123
  key_handle: key-abc456
  pin_encrypted: ${KMS_ENCRYPTED_PIN}
EOF
```

**Key rotation**:
```bash
# Generate new key in HSM
esper-forge-admin rotate-key \
    --old-key key-abc456 \
    --generate-new

# Update certificate registry with new public key
# Old certificates remain valid (grandfathered)
# New certificates use new key
```

---

### Network Security

**Firewall rules**:
```bash
# Allow only necessary ports
ufw default deny incoming
ufw default allow outgoing
ufw allow 443/tcp  # HTTPS API
ufw allow 22/tcp from 10.0.0.0/8  # SSH from internal only
ufw enable
```

**API rate limiting**:
```yaml
# config.yml
rate_limiting:
  enabled: true
  default_limit: 100/hour
  burst: 10
  whitelist:
    - 10.0.0.0/8  # Internal networks
  blacklist:
    - 192.0.2.0/24  # Known bad actors
```

**DDoS protection**:
```yaml
# Use Cloudflare or AWS Shield
cloudflare:
  enabled: true
  zone_id: ${CLOUDFLARE_ZONE}
  challenge_on_suspicious: true
  rate_limit_threshold: 1000/minute
```

---

### Database Security

**Encryption at rest**:
```sql
-- PostgreSQL with encryption
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/server.crt';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/server.key';

-- Enable transparent data encryption (TDE)
-- (Enterprise PostgreSQL or AWS RDS)
```

**Access control**:
```sql
-- Principle of least privilege
CREATE ROLE esper_forge_api LOGIN PASSWORD 'strong_password';
GRANT SELECT, INSERT, UPDATE ON certificates TO esper_forge_api;
GRANT SELECT ON public_keys TO esper_forge_api;
REVOKE DELETE ON certificates FROM esper_forge_api;

-- Admin user separate
CREATE ROLE esper_forge_admin LOGIN PASSWORD 'admin_password';
GRANT ALL PRIVILEGES ON DATABASE esper_forge TO esper_forge_admin;
```

**Audit logging**:
```sql
-- Enable pgAudit extension
CREATE EXTENSION IF NOT EXISTS pgaudit;

ALTER SYSTEM SET pgaudit.log = 'all';
ALTER SYSTEM SET pgaudit.log_relation = on;

-- Logs go to syslog → SIEM
```

---

### Compliance

**SOC 2 Type II**:
- Annual audit required
- Access controls documented
- Incident response plan
- Disaster recovery tested
- Vendor management

**GDPR** (if EU users):
- Data minimization (anonymize learner IDs)
- Right to erasure (delete stories, keep certificates)
- Data portability (export certificates in standard format)
- Privacy by design (encryption, access controls)

**HIPAA** (if medical use):
- Business Associate Agreement (BAA)
- Encryption in transit and at rest
- Access logging
- Breach notification procedures

---

## Monitoring and Observability

### Metrics

**System metrics**:
```
- CPU usage per worker
- Memory usage per worker
- Disk I/O (database, storage)
- Network throughput
- Queue depth (pending jobs)
```

**Application metrics**:
```
- Certifications per hour
- Average processing time per layer
- Conservation law pass rate
- Certificate validation requests
- API response times (p50, p95, p99)
```

**Business metrics**:
```
- Learners served per day
- Stories certified per week
- Certificate verification rate
- User satisfaction (if collected)
```

**Prometheus configuration**:
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'esper-forge-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'esper-forge-workers'
    static_configs:
      - targets:
          - 'worker1:9100'
          - 'worker2:9100'
    scrape_interval: 15s
```

**Grafana dashboards**:
```
- System health overview
- Certification pipeline flow
- Conservation law violations (should be zero)
- Certificate issuance rate
- Error rate by layer
```

---

### Logging

**Structured logging**:
```python
import structlog

log = structlog.get_logger()

log.info(
    "certification_started",
    job_id="job_3f7a8b2c",
    artifact_type="literacy_narrative",
    learner_id="hash_anonymized"
)

log.info(
    "layer_completed",
    job_id="job_3f7a8b2c",
    layer="semantic_encoding",
    duration_seconds=4.2,
    semantic_drift=0.03
)

log.error(
    "conservation_violation",
    job_id="job_3f7a8b2c",
    layer="pivotgram_validation",
    violation_type="semantic_drift",
    drift_value=0.18,
    threshold=0.15
)
```

**Log aggregation**:
```yaml
# filebeat.yml (ship to Elasticsearch)
filebeat.inputs:
  - type: log
    paths:
      - /var/log/esper-forge/*.log
    json.keys_under_root: true
    json.add_error_key: true

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "esper-forge-%{+yyyy.MM.dd}"
```

---

### Alerting

**Critical alerts** (PagerDuty/OpsGenie):
```yaml
alerts:
  - name: "API Down"
    condition: up{job="esper-forge-api"} == 0
    duration: 2m
    severity: critical
    
  - name: "Conservation Law Violations"
    condition: rate(conservation_violations[5m]) > 0
    duration: 1m
    severity: critical
    
  - name: "Certificate Signing Failure"
    condition: rate(certificate_signing_errors[5m]) > 0
    duration: 1m
    severity: critical
```

**Warning alerts** (Slack):
```yaml
  - name: "High Queue Depth"
    condition: queue_depth > 100
    duration: 10m
    severity: warning
    
  - name: "Slow Processing"
    condition: avg(certification_duration_seconds) > 120
    duration: 15m
    severity: warning
```

---

## Backup and Disaster Recovery

### Backup Strategy

**Database backups**:
```bash
# Daily full backup
pg_dump esper_forge | gzip > backup_$(date +%Y%m%d).sql.gz

# Continuous WAL archiving (point-in-time recovery)
archive_command = 'cp %p /mnt/wal_archive/%f'
```

**Certificate registry backups**:
```bash
# Certificates are immutable, replicate to multiple locations
rsync -avz /var/lib/esper-forge/certificates \
    backup-server:/mnt/certificates/

# S3 for off-site (with versioning enabled)
aws s3 sync /var/lib/esper-forge/certificates \
    s3://esper-forge-certificates/ \
    --storage-class GLACIER
```

**Configuration backups**:
```bash
# Version control all configuration
git add /etc/esper-forge/
git commit -m "Configuration snapshot $(date)"
git push origin main
```

---

### Disaster Recovery

**RTO (Recovery Time Objective)**: 4 hours  
**RPO (Recovery Point Objective)**: 1 hour (database), 0 (certificates)

**Recovery procedure**:
```bash
# 1. Provision new infrastructure (use Terraform)
terraform apply -var-file=dr.tfvars

# 2. Restore database
gunzip < backup_latest.sql.gz | psql esper_forge_new

# 3. Restore certificate registry
rsync -avz backup-server:/mnt/certificates/ \
    /var/lib/esper-forge/certificates/

# 4. Update DNS (or load balancer)
# Point api.esper-forge.org to new infrastructure

# 5. Verify
curl https://api.esper-forge.org/health
# Should return healthy

# 6. Resume processing
systemctl start esper-forge-worker@{1..8}
```

**DR testing**:
- Quarterly failover drill
- Document recovery time
- Update procedures based on findings

---

## Scaling

### Horizontal Scaling

**Add workers**:
```bash
# On new server
apt-get install esper-forge-worker
systemctl enable esper-forge-worker@{1..16}
systemctl start esper-forge-worker@{1..16}

# Workers automatically join cluster via Redis
```

**Load balancing**:
```nginx
upstream esper_forge_backend {
    least_conn;  # Route to least busy server
    server api1.internal:8000 max_fails=3 fail_timeout=30s;
    server api2.internal:8000 max_fails=3 fail_timeout=30s;
    server api3.internal:8000 max_fails=3 fail_timeout=30s;
    server api4.internal:8000 max_fails=3 fail_timeout=30s;
}
```

**Auto-scaling** (Kubernetes):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: esper-forge-worker
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: esper-forge-worker
  minReplicas: 8
  maxReplicas: 64
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: queue_depth
        target:
          type: AverageValue
          averageValue: "10"
```

---

### Vertical Scaling

**Increase worker resources**:
```yaml
# Kubernetes pod spec
resources:
  requests:
    memory: "16Gi"  # Up from 8Gi
    cpu: "4"        # Up from 2
  limits:
    memory: "32Gi"
    cpu: "8"
```

**Optimize processing**:
```python
# Enable parallel operator execution
config.processing.parallel_operators = True
config.processing.max_parallel = 4

# Use GPU for tensor operations (if available)
config.processing.use_gpu = True
config.processing.gpu_memory_fraction = 0.8
```

---

### Geographic Distribution

**Multi-region deployment**:
```
Region 1 (US-East):
  - API servers
  - Workers
  - Database (primary)
  - Certificate registry (primary)

Region 2 (US-West):
  - API servers
  - Workers
  - Database (read replica)
  - Certificate registry (replica)

Region 3 (EU-Central):
  - API servers
  - Workers
  - Database (read replica)
  - Certificate registry (replica)
```

**Latency optimization**:
- Route users to nearest region (GeoDNS)
- Write certificates to primary, replicate async
- Cache certificates at edge (CloudFront/Fastly)

---

## Maintenance

### Routine Maintenance

**Weekly**:
- Review error logs
- Check disk space
- Verify backup integrity
- Review certificate issuance rate

**Monthly**:
- Update dependencies (security patches)
- Review access logs for anomalies
- Test DR procedures
- Capacity planning review

**Quarterly**:
- Full security audit
- Performance optimization review
- Update documentation
- User feedback analysis

---

### Upgrades

**Zero-downtime upgrade** (blue-green deployment):
```bash
# 1. Deploy new version to "green" environment
terraform apply -var="environment=green" -var="version=1.2.0"

# 2. Run smoke tests
curl https://api-green.internal/health
pytest tests/integration --env=green

# 3. Gradually shift traffic (10% → 50% → 100%)
# Via load balancer weight adjustment

# 4. Monitor metrics for regressions

# 5. If successful, decommission "blue"
# If issues, rollback by shifting traffic back to blue
```

**Database migrations**:
```bash
# Use Alembic for schema changes
alembic upgrade head

# For large tables, use online schema change tools
pt-online-schema-change \
    --alter "ADD COLUMN new_field TEXT" \
    D=esper_forge,t=certificates \
    --execute
```

---

## Troubleshooting

### Common Issues

#### Issue: "Conservation law violation"

**Symptoms**: Jobs fail at Layer 4

**Diagnosis**:
```bash
# Check logs
grep "conservation_violation" /var/log/esper-forge/worker.log

# Extract details
{
  "violation_type": "semantic_drift",
  "drift_value": 0.18,
  "threshold": 0.15,
  "affected_transformation": "grade_5_to_grade_12"
}
```

**Resolution**:
- Review transformation logic
- Check if input was corrupted
- Increase threshold if drift is acceptable (requires human review)
- Report bug if drift is unexpected

---

#### Issue: "HSM signing failure"

**Symptoms**: Certificates not generated, signing errors in logs

**Diagnosis**:
```bash
# Check HSM connectivity
esper-forge-admin hsm-status

# Check key availability
esper-forge-admin list-keys
```

**Resolution**:
- Verify HSM credentials
- Check network connectivity to HSM
- Ensure key hasn't expired
- Contact HSM vendor if hardware issue

---

#### Issue: "High queue depth"

**Symptoms**: Jobs taking long time to start processing

**Diagnosis**:
```bash
# Check queue depth
redis-cli llen esper_forge:job_queue

# Check worker status
systemctl status esper-forge-worker@*
```

**Resolution**:
- Add more workers (scale horizontally)
- Increase worker concurrency (if CPU/RAM available)
- Check for stuck jobs (may need manual intervention)

---

## Cost Optimization

### Cloud Costs

**Typical monthly costs** (mid-size news org):
```
Compute (API + workers): $1,500
Database (managed PostgreSQL): $800
Storage (S3/GCS): $200
Data transfer: $300
Monitoring (Datadog): $150
Total: ~$3,000/month
```

**Optimization strategies**:

**1. Reserved instances** (save 30-40%):
```bash
# Purchase 1-year reserved instances for baseline capacity
# Use spot/preemptible for burst capacity
```

**2. S3 lifecycle policies**:
```yaml
# Move old certificates to cheaper storage
- transition_days: 90
  storage_class: STANDARD_IA
- transition_days: 365
  storage_class: GLACIER
```

**3. Batch processing**:
```python
# Process multiple stories in single job (amortize overhead)
batch_size = 10  # Process 10 stories per worker invocation
# Reduces cold start costs
```

---

## Support and Community

### Getting Help

**Documentation**: https://docs.esper-forge.org

**Community forum**: https://community.esper-forge.org

**GitHub issues**: https://github.com/PaniclandUSA/Esper-Forge/issues

**Email support**: support@cyranoapp.org

**Enterprise support**: enterprise@cyranoapp.org (SLA-backed)

---

### Contributing

**Bug reports**:
1. Search existing issues
2. Provide minimal reproduction case
3. Include version, OS, configuration
4. Attach relevant logs (redact sensitive data)

**Feature requests**:
1. Describe use case
2. Explain why existing features insufficient
3. Propose API if applicable

**Code contributions**:
1. Read CONTRIBUTING.md
2. Fork repository
3. Create feature branch
4. Write tests
5. Submit pull request

---

## Conclusion

**ESPER-FORGE is production-ready** when deployed with:
- Appropriate infrastructure (see scenarios)
- Security hardening (HSM, encryption, access controls)
- Monitoring and alerting (metrics, logs, alerts)
- Backup and DR (tested procedures)
- Maintenance plan (upgrades, security patches)

**Start small**:
- Development deployment (single server)
- Pilot with limited users
- Gradually scale based on demand

**Measure success**:
- Certification throughput
- Conservation law pass rate (should be >95%)
- User satisfaction
- Cost per certification

**Iterate**:
- Gather feedback
- Optimize performance
- Add features based on real needs
- Document lessons learned

---

**4 million Americans achieve literacy.**

**With infrastructure that proves dignity is preserved.**

**This is how we deploy the future.**

---

## References

- [04-ARCHITECTURE.md](04-ARCHITECTURE.md) - System architecture
- [05-LITERACY-DEMO.md](05-LITERACY-DEMO.md) - Literacy application
- [06-JOURNALISM-DEMO.md](06-JOURNALISM-DEMO.md) - Journalism application
- [07-LEGAL-STANDARD.md](07-LEGAL-STANDARD.md) - Legal integration

**Infrastructure as Code**: https://github.com/PaniclandUSA/Esper-Forge/tree/main/infrastructure

**Deployment playbooks**: https://github.com/PaniclandUSA/Esper-Forge/tree/main/ansible

---

**The Cyrano de Bergerac Foundation**  
Website: [cyranoapp.org](https://cyranoapp.org)  
Technical support: support@cyranoapp.org  
Infrastructure consulting: devops@cyranoapp.org

---

*License: This documentation is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).*

*Attribution: Weber, J.J. II (2026). ESPER-FORGE: Mathematical Certification of Semantic Integrity. The Cyrano de Bergerac Foundation.*
