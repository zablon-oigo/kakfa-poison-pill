## Handling Kafka Poison Pill
This project demonstrates practical strategies for detecting and mitigating Kafka Poison Pills. A malformed or problematic messages that can break consumers.
It showcases how to keep your consumers resilient while providing:

- Real-time alerting using Alertmanager
- Monitoring dashboards through Grafana
- Metrics collection via Prometheus
- Dead Letter Queue (DLQ) handling

#### Archictecture Diagram
<img width="1201" height="361" alt="prometheus drawio" src="https://github.com/user-attachments/assets/b8c5458e-21ef-4e0e-99b8-75c9f7aaf40d" />


#### Prequisites
Before running the project , ensure you have the following installed:
|  Tool | Version  | Purpose  |
|---|---|---|
|  Java |  11+ |  Runtime for Kafka |
|  Python | 3.9+  | Running FastAPI Backend   |
|  Kafka | 4.0.0+  | Distributed Event Streaming   |
|  Prometheus |  Latest |  Metric Collection |
|  AlertManager | Latest  | Notifications  |
|  Grafana | Latest  | Visual Monitoring   |
|  httpie | Latest  | API Testing   |
|  Uv | Latest  | Python Package Management   |


#### Setup Guide
1.Clone the project
```bash
git clone https://github.com/zablon-oigo/kakfa-poison-pill.git
```
2.Run FastAPI in development mode
```bash
fastapi dev
```
3.Check health
```bash
http GET http://localhost:8000
```
4.Post data
```bash
http POST http://localhost:8000/marks  id=1 score="20"
```

#### Prometheus & AlertManager Configuration
1.Update prometheus.yml file
```bash
# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets: ['localhost:9096']

rule_files:
  - "/etc/prometheus/alerting_rules.yml"

scrape_configs:
  - job_name: 'kafka-consumer'
    static_configs:
      - targets: ['localhost:9200']
```
2.Update your alertmanager.yml (replace commented fields):
```bash
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: ''               # Sender Email
  smtp_auth_username: ''      # Email Username
  smtp_auth_password: ''      # Email Password
  smtp_require_tls: true

route:
  receiver: 'kafka-alert-email'

receivers:
  - name: 'kafka-alert-email'
    email_configs:
      - to: ''                # Receiver Email
        send_resolved: true
        subject: '{{ .Status | toUpper }}: Kafka Poison Pill Alert'
        html: |
          <h2>{{ .Status | toUpper }} Alert: {{ .CommonLabels.alertname }}</h2>
          <p><strong>Instance:</strong> {{ .CommonLabels.instance }}</p>
          <p><strong>Severity:</strong> {{ .CommonLabels.severity }}</p>
          <h3>Details:</h3>
          <ul>
          {{ range .Alerts }}
            <li>{{ .Annotations.description }}</li>
            <li><strong>Starts At:</strong> {{ .StartsAt }}</li>
          {{ end }}
          </ul>
```
3.Create alerting_rules.yml inside Prometheus directory:
```bash
groups:
  - name: consumer_alerts
    rules:
      - alert: PoisonPillDetected
        expr: rate(poison_pills_total[1m]) > 0
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "CRITICAL: Kafka Consumer detected a poison pill."
          description: "Bad messages detected in 'marks' topic. Check 'marks_dlq' topic in Kafka."
```

### Testing the Consumers
#### Test Failing Consumer
1.Run consumer client
```bash
py consumer.py
```
2.Send data
```bash
http POST http://loclahost:8000/marks id=10 score="50"
```
3.Send data again
```bash
http POST http://localhost:8000/marks id=11 score=77
```
Result: consumer crashes due to poison pill.

#### Test Safe Consumer
1.Run consumer client
```bash
py consumer_safe.py
```
2.Send data
```bash
http POST http://loclahost:8000/marks id=12 score="60"
```
2.Send data again
```bash
http POST http://loclahost:8000/marks id=14 score=80
```
Result:
- App continues processing.
- Poison pill redirected to DLQ


#### Verify Kafka Topics
```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```
Ensure topic `marks_dlq` exists.
