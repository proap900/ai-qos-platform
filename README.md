<a name="top"></a>
# AI QoS Platform — ML-Driven Network Bandwidth Prediction

![Build](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue)

This repository demonstrates a backend-focused ML + DevOps platform that trains, serves, monitors, and automatically deploys an LSTM model to predict network bandwidth (QoS) using containerized microservices.

---

## Table of Contents

- [Overview](#overview)
- [What the Project Does](#what-the-project-does)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Usage](#api-usage)
- [CI/CD Flow](#cicd-flow)
- [Monitoring](#monitoring)
- [Learning Outcomes](#learning-outcomes)
- [Author](#author)

---

## Overview

The AI QoS Platform is a demonstration project showing how an ML model can be integrated into a production-style pipeline. It focuses on backend services, automated CI/CD, container orchestration, and monitoring.

The system predicts network bandwidth/Quality of Service (QoS) metrics from historical network parameters and exposes predictions via REST APIs.

## What the Project Does

- Trains and uses an LSTM model to predict network bandwidth
- Exposes prediction and health endpoints via FastAPI
- Separates concerns into microservices (API gateway and ML inference)
- Automates build, test, push, and deployment using Jenkins
- Deploys services to Kubernetes (Minikube for local testing)
- Supports automatic model and code updates with rolling deploys

## Architecture

Client (curl / Postman)
  → API Gateway (FastAPI) → ML Inference Service (FastAPI + LSTM model)

All services are containerized with Docker and orchestrated using Kubernetes.

## Technologies

**Backend & ML**: Python, FastAPI, TensorFlow/Keras, NumPy, scikit-learn

**DevOps & Infra**: Docker, Docker Hub, Jenkins, Kubernetes, Minikube, Ansible

**Monitoring**: Nagios (health-check based monitoring)

## Project Structure

```
ai-qos-platform/
├── Jenkinsfile
├── docker-compose.yml
├── README.md
├── deploy/
│   ├── ansible/
│   │   ├── deploy.yml
│   │   └── inventory
│   └── k8s/
│       ├── api-gateway-deployment.yaml
│       ├── api-gateway-service.yaml
│       ├── ml-inference-deployment.yaml
│       └── ml-inference-service.yaml
└── services/
    ├── api-gateway/
    └── ml-inference/
```

## Getting Started

### Prerequisites

- Docker
- Minikube
- kubectl
- Jenkins (optional for local dev)
- Python 3.9+

### Run Locally with Minikube

1. Start Minikube

```bash
minikube start
```

2. Apply the Kubernetes manifests

```bash
kubectl apply -f deploy/k8s/
```

3. Expose services (run each in a separate terminal)

```bash
minikube service api-gateway
minikube service ml-inference
```

4. Verify services

```bash
kubectl get svc
```

## API Usage

### Predict Bandwidth

**Endpoint**: `POST /predict`

**Request JSON**:

```json
{
  "packet_rate": [950, 1020, 980, 1100, 1080, 1150, 1200, 1180, 1220, 1250],
  "bandwidth_util": [45, 50, 48, 55, 57, 60, 62, 61, 63, 65],
  "rtt_variance": [4, 5, 4.5, 6, 5.5, 6.2, 6.5, 6.1, 6.8, 7]
}
```

**cURL example**:

```bash
curl -X POST http://<API_GATEWAY_URL>/predict \
  -H "Content-Type: application/json" \
  -d '{"packet_rate":[950,1020,980,1100,1080,1150,1200,1180,1220,1250],"bandwidth_util":[45,50,48,55,57,60,62,61,63,65],"rtt_variance":[4,5,4.5,6,5.5,6.2,6.5,6.1,6.8,7]}'
```

**Sample response**:

```json
{
  "predicted_bandwidth": 72.84,
  "unit": "Mbps"
}
```

> Prediction depends on the currently deployed trained model.

### Health Check

**Endpoint**: `GET /health`

Use the health endpoint for Jenkins smoke tests, Kubernetes readiness probes, and Nagios checks.

## CI/CD Flow

1. Push to GitHub
2. Jenkins pipeline builds service images
3. Pipeline runs container health checks
4. Images pushed to Docker Hub
5. Kubernetes deployments updated (rolling updates)

This pipeline enables zero-downtime updates and automatic model deployment.

## Monitoring

The services expose `/health` endpoints to support Nagios HTTP checks for availability and alerting.

## Learning Outcomes

- ML model serving in production-style systems
- Microservice-based backend design
- Docker image lifecycle management
- CI/CD automation with Jenkins
- Kubernetes service orchestration
- Practical MLOps concepts

## Author
Aayush (proap900) — AI / ML / DevOps Academic & Portfolio Project

---

[Back to Top](#top)
