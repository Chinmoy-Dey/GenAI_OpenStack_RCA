import gradio as gr
import requests


#Manoj: Importing the rag functions
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.rca_huggingface import ragFunction_hf
from src.rca_openai import ragFunction_openai
from src.logbert_pretrained import adbert


# Define the endpoint URL
API_URL = "http://localhost:8000"
PREDICT_ENDPOINT = f"{API_URL}/predict"
RCA_ENDPOINT = f"{API_URL}/root_cause_analysis"
RCA_GENERATION = f"{API_URL}/root_cause_generate"

#Manoj- adding the Ananmoly endpoint 
ANAMOLY_ENDPOINT = f"{API_URL}/anamolydetect"
RCA_HF_ENDPOINT = f"{API_URL}/rca_hf"
RCA_OPENAI_ENDPOINT = f"{API_URL}/rca_openai"

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

"""
def rca_hf(logs):
    print(logs)
    log_list = logs.splitlines()
    print("Sending to API:", {"logs": log_list})
    response = requests.post(RCA_HF_ENDPOINT, json={"logs": log_list})
    if response.status_code == 200:
        data = response.json()
        anomalies = data["anomalies"]
        root_causes = data["root_causes"]
        return f"Anomalies: {anomalies}\nRoot Causes: {root_causes}"
    return "Error: Unable to connect to the RCA service."
    """
def ad_bert():
    #print("Sending to API:", {"logs": logs})
    response = adbert()
    return response


def rca_hf(logs):
    print("Sending to API:", {"logs": logs})
    response = ragFunction_hf(logs)
    return response


def rca_openai(logs):
    print("Sending to API:", {"logs": logs})
    response = ragFunction_openai(logs)
    return response


# Define functions for each button
def button_1_action():
    return "Button 1 was clicked!"

with gr.Blocks() as demo:
    btn1 = gr.Button("Button 1")
    output = gr.Textbox(label="Output")
    
    btn1.click(button_1_action, inputs=None, outputs=output)
    

# Define the Gradio interface
interface = gr.TabbedInterface(
        [
        gr.Interface(
            fn=ad_bert,
            #inputs=gr.Textbox(lines=1, placeholder="Paste logs here..."),
            inputs = None,
            outputs="text",
            title="anamoly detect",
            description="detect anamolies in the log."
        ),

        gr.Interface(
            fn=rca_hf,
            inputs=gr.Textbox(lines=10, placeholder="Paste logs here..."),
            outputs="text",
            title="Root Cause Analysis with Hugging face model",
            description="Root cause analysis."
        ),

        gr.Interface(
            fn=rca_openai,
            inputs=gr.Textbox(lines=10, placeholder="Paste logs here..."),
            outputs="text",
            title="Root Cause Analysis with OpenAI model",
            description="Root cause analysis."
        ),




    ],
    #tab_names=["Anomaly Detection", "Root Cause Analysis",  "Issue Explainer", "Anamoly detect", "Root Cause Analysis with HF", "Root cause analysis with Open AI"]
    tab_names=["Anamoly detect", "Root Cause Analysis with HF", "Root cause analysis with Open AI"]
)
if __name__ == "__main__":
    #interface.launch(share=True)
    interface.launch(share=True)

