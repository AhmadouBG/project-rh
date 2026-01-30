from datadog import statsd

def send_payroll_failure_rate(day, taux_echec):
    """
    Send payroll failure KPI to Datadog as a gauge.
    Each 'day' is sent as a tag for filtering.
    """
    statsd.gauge(
        "kpi.payroll.failure_rate",
        taux_echec,
        tags=[f"day:{day}"]
    )
