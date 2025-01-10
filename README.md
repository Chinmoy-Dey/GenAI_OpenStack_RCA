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

```bash
   git clone https://github.com/Chinmoy-Dey/GenAI_OpenStack_RCA.git
   cd GenAI_OpenStack_RCA
   python -m venv venv
   cd venv/Scripts
  ./activate
   cd ../..
   pip install -r .\requirements.txt
   cd ui
   python app.py
```

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

.
├── CODEOWNERS
├── Dockerfile -> docker/Dockerfile
├── Project Status.xlsx
├── README.md
├── build_and_test_docker.sh
├── ci_cd
│   ├── deployment_script.sh
│   └── github_workflow.yml
├── config.yaml
├── data
│   ├── OpenStack_2k.log
│   ├── OpenStack_2k.log_structured.csv
│   ├── OpenStack_2k.log_templates.csv
│   └── context_kb.pdf
├── docker
│   ├── Dockerfile
│   └── docker-compose.yml
├── docker-compose.yml -> docker/docker-compose.yml
├── notebooks
│   ├── ClearML.ipynb
│   ├── LangGraphLearning.ipynb
│   ├── RAG_OPENAI_ver2.ipynb
│   ├── RCA_Huggingface.ipynb
│   ├── RCA_OPENAILLM.ipynb
│   ├── bert_ver2.ipynb
│   ├── context_kb.docx
│   ├── context_kb.pdf
│   ├── deeplog.ipynb
│   └── model_exploration.ipynb
├── requirements.txt
├── run.sh
├── service_startup.log
├── setup.py
├── setup_venv.sh
├── src
│   ├── __init__.py
│   ├── anomaly_detection.py
│   ├── data_preprocessing.py
│   ├── data_processing
│   │   └── log.txt
│   ├── export.py
│   ├── guardrails.py
│   ├── logbert_pretrained.py
│   ├── model.py
│   ├── model_architecture
│   │   ├── __init__.py
│   │   └── log_anomaly_detector.py
│   ├── model_files
│   │   └── LogAnomalyDetector
│   │       ├── model.pth
│   │       ├── special_tokens_map.json
│   │       ├── tokenizer_config.json
│   │       └── vocab.txt
│   ├── rca_huggingface.py
│   ├── rca_openai.py
│   ├── root_cause_analysis.py
│   └── utils.py
├── tests
│   ├── __init__.py
│   ├── test_anomaly_detection.py
│   ├── test_model.py
│   ├── test_preprocessing.py
│   └── test_root_cause_analysis.py
└── ui
    ├── api.py
    └── app.py

```
