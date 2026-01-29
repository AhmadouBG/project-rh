def payroll_failure_alert(kpi_results, threshold=5):
    alerts = []
    for row in kpi_results:
        print(row['day'], row['taux_echec'])
        if row["taux_echec"] > threshold:
            alerts.append({
                "day": row["day"],
                "alert": "Payroll failure rate exceeded threshold",
                "value": row["taux_echec"]
            })

    return alerts
