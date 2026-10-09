import time
import os
import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LinearRegression

# Read Slack webhook securely from an environment variable
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(message):
    """Send a predictive incident alert to Slack."""

    if not SLACK_WEBHOOK_URL:
        print(
            "Slack alert skipped: "
            "SLACK_WEBHOOK_URL is not configured."
        )
        return

    payload = {
        "text": (
            "🚨 PREDICTIVE INCIDENT MANAGEMENT ALERT 🚨\n"
            f"{message}"
        )
    }

    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            print("✅ Slack alert sent successfully.")
        else:
            print(
                f"❌ Failed to send Slack alert: "
                f"HTTP {response.status_code}"
            )

    except requests.RequestException as e:
        print(f"❌ Error connecting to Slack: {e}")


def evaluate_risk():
    """Analyze collected memory metrics and predict future memory usage."""

    csv_file = "metrics.csv"

    if not os.path.exists(csv_file):
        print("⏳ Waiting for metrics.csv to be created...")
        return False

    try:
        df = pd.read_csv(csv_file)

        if "memory_usage_mb" not in df.columns:
            print("❌ Required column 'memory_usage_mb' is missing.")
            return False

        # Remove missing and invalid memory measurements
        df["memory_usage_mb"] = pd.to_numeric(
            df["memory_usage_mb"],
            errors="coerce"
        )
        df = df.dropna(subset=["memory_usage_mb"])

        if len(df) < 5:
            print("📊 Collecting baseline data points...")
            return False

        y = df["memory_usage_mb"].to_numpy(dtype=float)

        if not np.isfinite(y).all():
            print("❌ Metrics contain invalid memory values.")
            return False

        X = np.arange(len(y)).reshape(-1, 1)

        # Train a simple Linear Regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict memory usage approximately 20 seconds ahead
        future_steps = 10
        future_X = np.array([[len(y) - 1 + future_steps]])
        predicted_memory = float(model.predict(future_X)[0])

        # Critical memory threshold for this demonstration
        CRITICAL_LIMIT_MB = 50.0

        current_mem = float(y[-1])

        print(
            f"📈 Current: {current_mem:.2f} MB | "
            f"Predicted in {future_steps * 2}s: "
            f"{predicted_memory:.2f} MB | "
            f"Limit: {CRITICAL_LIMIT_MB:.2f} MB"
        )

        if predicted_memory >= CRITICAL_LIMIT_MB:
            alert_msg = (
                "Service: FastAPI App\n"
                "Issue: High memory usage is predicted.\n"
                f"Current Memory: {current_mem:.2f} MB\n"
                f"Projected Memory: {predicted_memory:.2f} MB "
                f"in approximately {future_steps * 2} seconds\n"
                f"Critical Limit: {CRITICAL_LIMIT_MB:.2f} MB\n"
                "Recommended Action: Investigate memory usage "
                "and consider scaling or restarting the service."
            )

            print(
                "\n🚨 [PROACTIVE INCIDENT ALERT] "
                "Sending notification to Slack..."
            )

            send_slack_alert(alert_msg)
            return True

        return False

    except (OSError, pd.errors.ParserError, ValueError) as e:
        print(f"❌ Error reading or processing metrics: {e}")
        return False


if __name__ == "__main__":
    print("🤖 Starting Predictive Incident Monitor...")
    print("📊 Monitoring memory usage with Linear Regression.")
    print("🔔 Slack notifications are enabled when configured.")
    print("Press Ctrl+C to stop monitoring.\n")

    try:
        while True:
            is_critical = evaluate_risk()

            if is_critical:
                # Pause longer after a critical prediction
                time.sleep(30)
            else:
                time.sleep(2)

    except KeyboardInterrupt:
        print("\n🛑 Predictive Incident Monitor stopped.")