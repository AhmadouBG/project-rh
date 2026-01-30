from pymongo import MongoClient
from alerts.alert_doc import document_average_size_by_type_alert, document_size_alert
from alerts.payroll_failure_rate import payroll_failure_alert
from kpi.application_kpi import flux_daily_application_by_client
from kpi.client_kpi import count_active_clients_with_recent_payrolls, get_new_clients_by_month
from kpi.doc_kpi import document_average_size_by_type
from kpi.payroll_kpi import count_payroll_by_client_month, failure_rate_payroll_by_client_month
import os
from monitoring.datadog_init import init_datadog
from monitoring.datadog_metric import send_payroll_failure_rate

def main():
    # =========================
    # Connect to MongoDB
    # =========================
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    db = client["database_rh"]

    # =========================
    # KPI Clients
    # =========================
    kpi_active_clients = list(db.clients.aggregate(count_active_clients_with_recent_payrolls(30)))
    kpi_new_clients = list(db.clients.aggregate(get_new_clients_by_month()))

    # =========================
    # KPI Payrolls
    # =========================
    kpi_payroll_count = list(db.payrolls.aggregate(count_payroll_by_client_month()))
    kpi_payroll_failure = list(db.payrolls.aggregate(failure_rate_payroll_by_client_month()))

    # =========================
    # KPI Applications
    # =========================
    kpi_applications = list(db.applications.aggregate(flux_daily_application_by_client()))

    # =========================
    # KPI Documents (Alerts)
    # =========================
    kpi_doc_alerts = list(db.documents.aggregate(document_average_size_by_type_alert()))

    # =========================
    # Display KPI Results
    # =========================
    print("\n=== Clients actifs ===")
    for row in kpi_active_clients:
        print(f"Clients actifs (30 jours): {row['active_clients']}")

    print("\n=== Nouveaux clients par mois ===")
    for row in kpi_new_clients:
        print(f"Mois: {row['_id']}, Nouveaux clients: {row['new_clients']}")

    print("\n=== Payrolls par client et mois ===")
    for row in kpi_payroll_count:
        print(f"Client: {row['client_name']}, Mois: {row['month']}, Nombre de fiches de paie: {row['payroll_count']}")

    print("\n=== Taux d'échec des payrolls par mois ===")
    for row in kpi_payroll_failure:
        print(f"Client: {row['client_id']}, Mois: {row['month']}, Taux d'échec: {row['failure_rate']:.2f}%")

    print("\n=== Applications quotidiennes par client ===")
    for row in kpi_applications:
        print(f"Client: {row['client_name']}, Jour: {row['day']}, Nombre d'applications: {row['application_count']}")

    print("\n=== Alertes sur les documents ===")
    for row in kpi_doc_alerts:
        print(f"Type de document: {row['type']}, Taille moyenne: {row['avg_size']:.2f} bytes")

    # =========================
    # Alerts
    # =========================
    payroll_alerts = payroll_failure_alert(kpi_payroll_failure, threshold=5)
    print("\n=== Alertes Taux d'échec Payroll ===")
    for alert in payroll_alerts:
        print(f"Alerte le {alert['day']}: {alert['alert']} (Valeur: {alert['value']:.2f}%)")

    doc_size_alerts = document_size_alert(kpi_doc_alerts)
    print("\n=== Alertes Taille des Documents ===")
    for alert in doc_size_alerts:
        print(f"Alerte pour le type {alert['type']}: {alert['alert']} (Taille moyenne: {alert['avg_size']:.2f} bytes)")

    # =========================
    # Send metrics to Datadog
    # =========================
    # Initialize Datadog
    init_datadog()
    for row in payroll_alerts:
        send_payroll_failure_rate(
            day=row["day"],
            taux_echec=row["failure_rate"]
        )






if __name__ == "__main__":
    main()
