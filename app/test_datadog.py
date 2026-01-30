from datadog import initialize, statsd

# Initialize DogStatsD connection to Datadog Agent
initialize(statsd_host="datadog", statsd_port=8125)

# Send a test metric
statsd.gauge("test.metric", 42)
print("Sent test metric")
