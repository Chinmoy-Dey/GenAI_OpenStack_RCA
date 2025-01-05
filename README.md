#PR raise method
need reviewer and owner's approval

# GenAI OpenStack log RCA
This project aims to develop an interactive root cause analysis (RCA) system using Generative AI to understand and explain incidents in IT departments. . Generative AI can automate and enhance this process by analyzing system logs and performance data, detecting patterns, and explaining potential root causes interactively. 
# OpenStack Log Anomaly Detection and Root Cause Analysis System

## Overview
This project provides a comprehensive solution for detecting anomalies and performing root cause analysis on OpenStack logs using advanced machine learning techniques, specifically LogBERT and advanced anomaly detection algorithms.

## Features
- LogBERT-based log embedding and analysis
- Advanced anomaly detection with multiple techniques
- Root Cause Analysis (RCA) using graph-based methods
- Gradio interactive web interface
- Docker and GitHub Actions deployment
- Guardrails for ensuring model reliability

## Prerequisites
- Python 3.9+
- Docker (optional, but recommended)
- GitHub Account (for CI/CD)
- Docker Hub Account (for image deployment)

### Local Setup
1. Clone the repository:
```bash
git clone https://github.com/Chinmoy-Dey/GenAI_OpenStack_RCA.git
cd GenAI_OpenStack_RCA
touch file1.py
git add file1.py
git commit -m "Add file1.py"
git push -f origin main
git log # check the commit history https://github.com/Chinmoy-Dey/GenAI_OpenStack_RCA.git
```
### Run locally
```bash
   sh run.sh
```

   2  git clone https://github.com/Chinmoy-Dey/GenAI_OpenStack_RCA.git
   3 ls
   4 cd .\GenAI_OpenStack_RCA\
   5 ls
   6 python -m venv venv
   7 cd venv
   8 ls
   9 cd Scripts
  10 ls
  11 .\activate
  12 cd ../..
  13 ls
  14 pip install -r .\requirements.txt
  15 ls
  16 cd ui
  17 ls
  18 python app.py


## Installation
Install dependencies:
```bash
   pip install -r requirements.txt
```
## Run test
```bash
   pytest tests/
```

```
   Error connecting to server.
   Timeout occurred while processing request.
   Operation completed successfully.
```
## Test the Application
### Access the Gradio UI: Open your browser and navigate to 
```
   http://localhost:7860
```

[ open APP Locally ](http://localhost:7860)


### Test the FastAPI Endpoint: Send a POST request to API endpoint using Postman or curl 
```
   http://localhost:8000/predict

```

```
   curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"log": "Success"}'
   curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"log": "Failure"}'

   curl -X POST "http://localhost:8000/root_cause_analysis" -H "Content-Type: application/json" -d '{"logs": ["openstack log with error", "app log entry", "Timeout occurred"]}'


```
## Dockerize the Application
### Build docker image
```
   ./build_and_test_docker.sh
```
### Run docker container 
```
   docker run -p 8000:8000 -p 7860:7860 anomaly-detector-rca-app

```
### Push the Docker Image to a Registry
```
   docker tag anomaly-detector-app chinmoydey/anomaly-detector-app:latest
   docker login
   docker push chinmoydey/anomaly-detector-app:latest

```
## Deployment
```bash

```

# Code structure
```
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── model.py
│   ├── anomaly_detection.py
│   ├── root_cause_analysis.py
│   ├── guardrails.py
│   └── utils.py
│
├── notebooks/
│   └── model_exploration.ipynb
│
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py
│   ├── test_model.py
│   └── test_anomaly_detection.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── ci_cd/
│   ├── github_workflow.yml
│   └── deployment_script.sh
│
├── requirements.txt
├── README.md
├── setup.py
└── config.yaml
```
