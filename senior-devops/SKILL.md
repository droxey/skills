---
name: senior-devops
description: Use when handling CI/CD, infra automation, containerization, and cloud operations.
created_at: '2026-05-15T16:43:15.966146+00:00'
updated_at: '2026-05-15T16:43:15.966146+00:00'
maturity: 0
---

# Senior Devops

Complete toolkit for senior devops with modern tools and best practices.

## Quick Start

### Main Capabilities

This skill provides three core capabilities through documented, reviewable workflows:

```bash
# Pipeline: add a reviewed GitHub Actions or CircleCI workflow with build, test, and deploy stages.
# Terraform: create the provider module, then run init, validate, and plan before applying.
# Deployment: use the target platform's rollout and rollback commands with health-check gates.
```

## Core Capabilities

### 1. Pipeline Generator

Scaffolds CI/CD pipeline configurations for GitHub Actions or CircleCI, with stages for build, test, security scan, and deploy.

**Example — GitHub Actions workflow:**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  build-docker:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    needs: build-docker
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service app-service \
            --force-new-deployment
```

**Usage:**
Define the workflow in the target repository and review its generated diff before enabling deployments.

### 2. Terraform Scaffolder

Generates, validates, and plans Terraform modules. Enforces consistent module structure and runs `terraform validate` + `terraform plan` before any apply.

**Example — AWS ECS service module:**
```hcl
# modules/ecs-service/main.tf
resource "aws_ecs_task_definition" "app" {
  family                   = var.service_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.cpu
  memory                   = var.memory

  container_definitions = jsonencode([{
    name      = var.service_name
    image     = var.container_image
    essential = true
    portMappings = [{
      containerPort = var.container_port
      protocol      = "tcp"
    }]
    environment = [for k, v in var.env_vars : { name = k, value = v }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group        = "/ecs/${var.service_name}"
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "app" {
  name            = var.service_name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = var.service_name
    container_port   = var.container_port
  }
}
```

**Usage:**
Create the module in the target infrastructure repository, then run `terraform init`, `terraform validate`, and `terraform plan`.

### 3. Deployment Manager

Orchestrates deployments with blue/green or rolling strategies, health-check gates, and automatic rollback on failure.

**Example — Kubernetes blue/green deployment (blue-slot specific elements):**
```yaml
# k8s/deployment-blue.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  labels:
    app: myapp
    slot: blue      # slot label distinguishes blue from green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      slot: blue
  template:
    metadata:
      labels:
        app: myapp
        slot: blue
    spec:
      containers:
        - name: app
          image: ghcr.io/org/app:1.2.3
          readinessProbe:       # gate: pod must pass before traffic switches
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

**Usage:**
Use your platform's deployment tooling to deploy to staging, wait for health checks, then promote to production. Keep the previous revision available for immediate rollback.

## Development Workflow

### 1. Infrastructure Changes (Terraform)

```bash
# Validate and plan — review diff before applying
terraform -chdir=infra init
terraform -chdir=infra validate
terraform -chdir=infra plan -out=tfplan

# Apply only after plan review
terraform -chdir=infra apply tfplan

# Verify resources are healthy
aws ecs describe-services --cluster production --services app-service \
  --query 'services[0].{Status:status,Running:runningCount,Desired:desiredCount}'
```

### 2. Application Deployment

```bash
# Build and tag image
docker build -t ghcr.io/org/app:$(git rev-parse --short HEAD) .
docker push ghcr.io/org/app:$(git rev-parse --short HEAD)

# Verify pods are running
kubectl get pods -n production -l app=myapp
kubectl rollout status deployment/app-blue -n production

# Switch traffic after verification
kubectl patch service app-svc -n production \
  -p '{"spec":{"selector":{"slot":"blue"}}}'
```

### 3. Rollback Procedure

```bash
# Roll back via kubectl
kubectl rollout undo deployment/app -n production
kubectl rollout status deployment/app -n production

# Verify rollback succeeded
kzrectl get pods -n production -l app=myapp
curl -sf https://app.example.com/healthz || echo "ROLLBACK FAILED — escalate"
```

## Troubleshooting

Inspect deployment events, pod logs, health checks, and the most recent rollout
revision before escalating.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; no runnable asset or tests yet.

## Purpose

Provide comprehensive DevOps coverage across CI/CD, containers, and cloud.

## Inputs

The infrastructure or deployment problem and the target environment.

## Outputs

Robust configuration, automation, and operational guidance.

## Example

Design and apply a containerized deployment pipeline with health checks for a service.

## Success criteria

The delivered change is production-safe, reproducible, and documented.