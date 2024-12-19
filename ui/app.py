import gradio as gr
import requests


# Define the endpoint URL
API_URL = "http://localhost:8000"
PREDICT_ENDPOINT = f"{API_URL}/predict"
RCA_ENDPOINT = f"{API_URL}/root_cause_analysis"
RCA_GENERATION = f"{API_URL}/root_cause_generate"

def predict(log):
    # Send a POST request to the FastAPI endpoint
    response = requests.post(PREDICT_ENDPOINT, json={"log": log})
    if response.status_code == 200:
        return "Anomaly Detected" if response.json()["prediction"] == 1 else "Log is Normal"
    return "Error: Unable to connect to the prediction service."

def root_cause_analysis(logs):
    log_list = logs.splitlines()
    print("Sending to API:", {"logs": log_list})
    response = requests.post(RCA_ENDPOINT, json={"logs": log_list})
    if response.status_code == 200:
        data = response.json()
        anomalies = data["anomalies"]
        root_causes = data["root_causes"]
        return f"Anomalies: {anomalies}\nRoot Causes: {root_causes}"
    return "Error: Unable to connect to the RCA service."

def root_cause_generation(logs):
    logs = logs.splitlines()
    response = requests.post(RCA_GENERATION, json={"logs": logs})
    if response.status_code == 200:
        data = response.json()
        anomalies = data["anomalies"]
        root_causes = data["root_causes"]
        result = "\n".join([f"Log {i}: {root_causes[str(i)]}" for i, a in enumerate(anomalies) if a == 1])
        return result or "No anomalies detected."
    return f"Error: {response.status_code} - {response.text}"

# Define the Gradio interface
interface = gr.TabbedInterface(
    [
        gr.Interface(
            fn=predict,
            inputs=gr.Textbox(lines=5, placeholder="Enter log text here..."),
            outputs="text",
            title="Log Anomaly Detection",
            description="Detect anomalies in logs using LogBERT.",
        ),
        gr.Interface(
            fn=root_cause_analysis,
            inputs=gr.Textbox(lines=10, placeholder="Enter multiple log entries, one per line...", label="Logs"),
            outputs="text",
            title="Root Cause Analysis",
            description="Perform RCA for logs and detected anomalies.",
        ),
       gr.Interface(
            fn=root_cause_generation,
            inputs=gr.Textbox(lines=10, placeholder="Paste logs here..."),
            outputs="text",
            title="Issue Explainer",
            description="Detect anomalies in logs and explain root causes."
        ), 
    ],
    tab_names=["Anomaly Detection", "Root Cause Analysis",  "Issue Explainer"]
)
if __name__ == "__main__":
    #interface.launch(share=True)
    interface.launch(share=True)

