# Project Checklist

## Step 1 — Planning, Environment, and Git

- [x] Check operating system
- [x] Check processor and memory
- [x] Check available development tools
- [x] Verify Git installation and identity
- [x] Verify Docker
- [x] Verify kubectl
- [x] Check current Kubernetes status
- [x] Install Python 3.12
- [x] Verify VS Code
- [x] Create project directory
- [x] Initialize local Git repository
- [x] Create README
- [x] Create .gitignore
- [x] Create GitHub repository
- [x] Make first documentation commit
- [x] Push repository to GitHub

## Step 2 — FastAPI Application

- [x] Create Python virtual environment
- [x] Define project dependencies
- [x] Create FastAPI application
- [x] Add /health endpoint
- [x] Test with Swagger UI
- [x] Add first automated test
- [x] Verify application logs

## Step 3 — PostgreSQL and Persistence

- [ ] Define application data model
- [ ] Start PostgreSQL
- [ ] Connect FastAPI to PostgreSQL
- [ ] Configure database credentials using environment variables
- [ ] Add database migrations
- [ ] Verify data persists after application restart

## Step 4 — Application CRUD

- [ ] Create job application
- [ ] Get one job application
- [ ] List job applications
- [ ] Update job application
- [ ] Delete job application
- [ ] Add pagination or result limits
- [ ] Add input validation
- [ ] Add success and failure tests

## Step 5 — Redis Cache and Fallback

- [ ] Connect Redis
- [ ] Cache application list
- [ ] Configure cache TTL
- [ ] Invalidate cache after data changes
- [ ] Add PostgreSQL fallback
- [ ] Test Redis failure behavior

## Step 6 — Docker and Compose

- [ ] Create API Dockerfile
- [ ] Run application as non-root user
- [ ] Create Docker Compose configuration
- [ ] Add PostgreSQL persistent volume
- [ ] Add .env.example
- [ ] Document local start, stop, logs, and cleanup

## Step 7 — Kubernetes Deployment

- [ ] Select local Kubernetes setup
- [ ] Create namespace
- [ ] Deploy API using raw YAML
- [ ] Deploy PostgreSQL
- [ ] Deploy Redis
- [ ] Configure Services
- [ ] Configure ConfigMap and Secret
- [ ] Configure persistent storage
- [ ] Define migration strategy
- [ ] Test application using port-forward

## Step 8 — Reliability

- [ ] Configure liveness probe
- [ ] Configure readiness probe
- [ ] Configure startup probe
- [ ] Configure CPU and memory requests
- [ ] Configure resource limits
- [ ] Test graceful shutdown
- [ ] Test rolling update
- [ ] Test Pod replacement

## Step 9 — Helm and HTTPS

- [ ] Convert manifests to Helm chart
- [ ] Configure values
- [ ] Add environment override example
- [ ] Configure routing
- [ ] Configure local TLS
- [ ] Test Helm install
- [ ] Test Helm upgrade
- [ ] Test Helm rollback

## Step 10 — Security and Autoscaling

- [ ] Configure NetworkPolicies
- [ ] Restrict PostgreSQL access
- [ ] Restrict Redis access
- [ ] Configure ServiceAccount
- [ ] Harden container security
- [ ] Verify repository contains no secrets
- [ ] Configure metrics
- [ ] Configure HPA
- [ ] Test scale-up and scale-down

## Step 11 — Failure Lab

- [ ] Test API Pod deletion
- [ ] Test invalid image tag
- [ ] Test incorrect database password
- [ ] Test incorrect probe configuration
- [ ] Test Redis outage
- [ ] Test NetworkPolicy failure
- [ ] Document diagnosis and recovery

## Step 12 — Frontend and Release

- [ ] Add job application form
- [ ] Add application table
- [ ] Add status update
- [ ] Add delete action
- [ ] Add loading, empty, and error states
- [ ] Serve frontend from FastAPI
- [ ] Perform fresh setup test
- [ ] Create architecture diagram
- [ ] Prepare demo evidence
- [ ] Document limitations
- [ ] Create v1.0.0 release
