# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose ports for FastAPI (8000) and Gradio (7860)
EXPOSE 8000
EXPOSE 7860

# Run both FastAPI and Gradio services
CMD ["sh", "-c", "uvicorn ui.api:app --host 0.0.0.0 --port 8000 & python ui/app.py"]