# Predictive Incident Management System

## Project Overview

The Predictive Incident Management System is a Python-based project that uses machine learning to predict potential application incidents by analyzing memory usage trends.

Instead of waiting for a resource issue to become critical, the system collects memory metrics, applies a Linear Regression model to forecast future memory usage, and sends an alert to Slack when the predicted value reaches a configured threshold.

The project demonstrates how machine learning can be integrated with application monitoring to support proactive incident detection.

## Objectives

* Monitor application memory usage.
* Collect and store performance metrics.
* Use machine learning to predict future memory consumption.
* Detect potential resource-related incidents before they occur.
* Send proactive incident notifications through Slack.
* Explore the integration of Python, APIs, machine learning, and containerization.

## Technologies Used

* **Python** – Core programming language.
* **FastAPI** – Application API and incident simulation endpoint.
* **Scikit-learn** – Linear Regression model for prediction.
* **Pandas and NumPy** – Metric processing and numerical operations.
* **psutil** – Process memory monitoring.
* **Requests** – Sending HTTP requests to Slack.
* **Slack Incoming Webhooks** – Incident notifications.
* **Docker and Docker Compose** – Containerization configuration.

## System Architecture

```text
FastAPI Application
        |
        v
Memory Usage Collector
        |
        v
   metrics.csv
        |
        v
Linear Regression Model
        |
        v
Predict Future Memory Usage
        |
        v
Compare Against Threshold
        |
        v
  Slack Notification
```

## Project Workflow

### Step 1: Create the FastAPI Application

Build a FastAPI application with a health-check endpoint and a `/leak` endpoint to simulate increasing memory consumption during testing.

### Step 2: Collect Memory Metrics

Create a collector script that monitors the application's memory usage using `psutil`. Store the collected measurements in a CSV file named `metrics.csv`.

### Step 3: Build the Prediction Model

Use Scikit-learn's Linear Regression algorithm to learn from the collected memory measurements and estimate future memory consumption.

### Step 4: Define the Critical Threshold

Configure a memory threshold of 50 MB for demonstration purposes. Compare the predicted memory usage against this threshold to identify potential incidents.

### Step 5: Integrate Slack Notifications

Configure a Slack Incoming Webhook through the `SLACK_WEBHOOK_URL` environment variable. When predicted memory usage reaches the threshold, send a notification containing the current usage and predicted value.

### Step 6: Test the System

Run the application, collector, and predictor in separate terminal windows. Call the `/leak` endpoint repeatedly to simulate increasing memory usage and observe the prediction output and Slack notifications.

### Step 7: Containerization

Use the Dockerfile and Docker Compose configuration to explore running the application and supporting components in containers. The containerized monitoring workflow requires its dependencies and metrics source to be configured correctly.

## Project Structure

```text
predictive-incident-demo/
├── app.py
├── collector.py
├── predictor.py
├── predictor_production.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/stelabiju/predictive-incident-alert.git
cd predictive-incident-alert
```

### 2. Create and Activate a Virtual Environment

For Windows CMD:

```cmd
python -m venv v
v\Scripts\activate
```

### 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 4. Configure the Slack Webhook

Set the webhook in your terminal session:

```cmd
set SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/NEW/WEBHOOK
```

Replace the example with your own webhook. Do not hardcode the URL or commit it to GitHub.

### 5. Start the Application

```cmd
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

### 6. Start the Collector

In a second terminal, activate the virtual environment and run:

```cmd
python collector.py
```

### 7. Start the Predictor

In a third terminal, activate the virtual environment, set the Slack webhook environment variable in that terminal, and run:

```cmd
python predictor.py
```

### 8. Simulate an Incident

Call the memory simulation endpoint multiple times:

```cmd
curl http://127.0.0.1:8000/leak
```

Observe the memory measurements, prediction logs, and Slack notifications.

## Expected Outcome

* Memory usage measurements are recorded in a CSV file.
* A Linear Regression model estimates future memory consumption.
* The predictor checks whether the forecast reaches the configured threshold.
* Slack receives an alert when a critical prediction is detected and the webhook is configured correctly.

## Limitations

* Linear Regression provides a simple forecast and may not capture complex memory usage patterns.
* The 50 MB threshold is intended for testing and should be adjusted for the target application.
* Predictions depend on the quality and quantity of collected metrics.
* The current predictor sends notifications; it does not itself execute automated scaling or restart operations.

## Future Enhancements

* Integrate Prometheus for centralized metrics collection.
* Add Grafana dashboards for monitoring and visualization.
* Improve forecasting with more advanced anomaly detection techniques.
* Deploy the system using Kubernetes.
* Explore controlled automated remediation for detected incidents.

