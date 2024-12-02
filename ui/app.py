import gradio as gr
import requests

# Define the endpoint URL
API_URL = "http://localhost:8000/predict"

def predict(log):
    # Send a POST request to the FastAPI endpoint
    response = requests.post(API_URL, json={"log": log})
    if response.status_code == 200:
        return "Anomaly Detected" if response.json()["prediction"] == 1 else "Log is Normal"
    return "Error: Unable to connect to the prediction service."


# Define the Gradio interface
interface = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(lines=5, placeholder="Enter log text here..."),
    outputs="text",
    title="Log Anomaly Detection",
    description="Detect anomalies in logs using LogBERT."
)

if __name__ == "__main__":
    interface.launch()
