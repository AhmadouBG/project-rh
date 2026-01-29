def payroll_failure_alert(kpi_results, threshold=5):
    alerts = []

    for row in kpi_results:
        if row["failure_rate"] > threshold:
            alerts.append({
                "day": row["day"],
                "alert": "Payroll failure rate exceeded threshold",
                "value": row["failure_rate"]
            })

    return alerts
