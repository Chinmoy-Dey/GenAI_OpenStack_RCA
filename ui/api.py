from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import logging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.anomaly_detection import predict_log
from src.anomaly_detection import predict_logs
from src.root_cause_analysis import analyze_root_cause
from src.root_cause_analysis import generate_root_cause

# Logger setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("fastapi")

# Define the FastAPI app
app = FastAPI()

# Request and response models
class LogRequest(BaseModel):
    log: str

class LogsRequest(BaseModel):
    logs: List[str]

class PredictionResponse(BaseModel):
    prediction: int

class RCAResponse(BaseModel):
    anomalies: List[int]
    root_causes: Dict[int, str]

# Endpoints
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: LogRequest):
    prediction = predict_log(request.log)
    return PredictionResponse(prediction=prediction)

@app.post("/root_cause_generate", response_model=RCAResponse)
async def analyze_logs(request: LogsRequest):
    """
    Analyze logs for anomalies and generate root causes.
    """
    logs = request.logs
    anomalies = predict_logs(logs)
    root_causes = generate_root_cause(logs, anomalies)
    return RCAResponse(anomalies=anomalies, root_causes=root_causes)

@app.post("/root_cause_analysis", response_model=RCAResponse)
async def root_cause_analysis(request: LogsRequest):
    print("Received logs:", request.logs)
    # Step 1: Predict anomalies for each log
    anomalies = [predict_log(log) for log in request.logs]
    # Step 2: Perform root cause analysis
    root_causes = analyze_root_cause(request.logs, anomalies)
    return RCAResponse(anomalies=anomalies, root_causes=root_causes)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation Error: {exc}")
    return JSONResponse(status_code=422, content={"message": str(exc)})
