from log_agent import analyze_logs
from anomaly_agent import detect_anomaly
from incident_agent import predict_incident
from notify import send_email

def main():
    with open("logs.txt", "r") as f:
        logs = f.read()

    print("Analyzing logs...")
    summary = analyze_logs(logs)
    print(summary)

    print("Detecting anomaly...")
    anomaly = detect_anomaly(summary)
    print(anomaly)

    print("Predicting incident...")
    prediction = predict_incident(anomaly)
    print(prediction)

    send_email("🚨 Incident Prediction Alert", prediction)

if __name__ == "__main__":
    main()
