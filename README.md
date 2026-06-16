# 🛡️ Network Security System

## Overview

Network Security System is an end-to-end Machine Learning and MLOps project designed to detect malicious network activity using machine learning techniques. The project follows a production-oriented workflow that includes data ingestion, validation, transformation, model training, experiment tracking, containerization, CI/CD automation, and cloud deployment.

The objective of this project is to demonstrate how machine learning models can be developed, tracked, packaged, and deployed using modern MLOps practices.

---

## Key Features

### Machine Learning Pipeline

* Automated Data Ingestion
* Data Validation
* Data Transformation
* Model Training
* Model Evaluation
* Prediction Pipeline

### MLOps Features

* MLflow Experiment Tracking
* Automated CI/CD Pipeline
* Docker Containerization
* Cloud Deployment on AWS

### Cloud Infrastructure

* AWS EC2 Instance
* AWS ECR Repository
* GitHub Actions Automation

---

## Project Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions CI/CD
    │
    ▼
Docker Image Build
    │
    ▼
AWS ECR Repository
    │
    ▼
AWS EC2 Instance
    │
    ▼
Docker Container
    │
    ▼
Network Security Application
```

---

## Project Structure

```text
Network_Security_System/
│
├── .github/
│   └── workflows/
│       └── CI-CD.yml
│
├── Network_Security/
│   │
│   ├── components/
│   │   │
│   │   ├── data_ingestion/
│   │   │   └── data_ingestion.py
│   │   │
│   │   ├── data_validation/
│   │   │   └── data_validation.py
│   │   │
│   │   ├── data_transformation/
│   │   │   └── data_transformation.py
│   │   │
│   │   ├── model_trainer/
│   │   |   └── model_trainer.py
│   │   
│   │   
│   │      
│   │
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   │
│   ├── entity/
│   ├── config/
│   ├── constants/
│   ├── utils/
│
│   ├── exception/
│   └── logger/
│
├── notebook/
├── templates/
├── app.py
├── Dockerfile
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

---


* Push to GitHub Repository

#### Actions

* Install Dependencies
* Build Docker Image
* Verify Build Process

### Continuous Deployment

#### Actions

* Push Docker Image to AWS ECR
* Pull Latest Image on EC2
* Run Updated Container
* Deploy Latest Application Version

---

## Docker Commands

### Build Image

```bash
docker build -t network-security .
```

### Run Container

```bash
docker run -p 5000:5000 network-security
```

### View Running Containers

```bash
docker ps
```

---

## AWS Deployment

### AWS Services Used

#### Amazon EC2

* Hosts the application.

#### Amazon ECR

* Stores Docker images.

### Deployment Flow

```text
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Docker Build
   │
   ▼
AWS ECR
   │
   ▼
AWS EC2
   │
   ▼
Docker Container
   │
   ▼
Application
```

---

## Future Improvements

### Monitoring

* Prometheus
* Grafana

### MLOps Enhancements
  Data Drift Detection
  Model Drift Detection
  Automated Retraining
### Infrastructure
    Terraform
    Kubernetes
    ArgoCD

---

## Learning Outcomes

Through this project, I gained hands-on experience in:

* Machine Learning Pipeline Development
* MLOps Best Practices
* MLflow Experiment Tracking
* Docker Containerization
* GitHub Actions CI/CD
* AWS Cloud Deployment
* Production-Level Project Structuring

---

## Author

### Vyom Soni

B.Sc. Computer Science and Data Analytics

Aspiring Machine Learning Engineer | MLOps Engineer | Data Scientist

---

## Project Highlights

* End-to-End Machine Learning Project
* Production-Oriented MLOps Workflow
* MLflow Integration
* Dockerized Deployment
* GitHub Actions CI/CD
* AWS ECR Integration
* AWS EC2 Deployment
* Clean and Modular Project Architecture
