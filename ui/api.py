from fastapi import FastAPI
from pydantic import BaseModel
from src.anomaly_detection import predict_log

# Define the FastAPI app
app = FastAPI()

# Request and response models
class LogRequest(BaseModel):
    log: str

class PredictionResponse(BaseModel):
    prediction: int

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: LogRequest):
    prediction = predict_log(request.log)
    return PredictionResponse(prediction=prediction)
