from datadog import initialize
import os

def init_datadog():
    options = {
        "statsd_host": os.getenv("DD_AGENT_HOST", "datadog"),
        "statsd_port": 8125,
    }
    initialize(**options)
