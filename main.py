from alerts.alert_doc import document_average_size_by_type_alert, document_size_alert
from alerts.payroll_failure_rate import payroll_failure_alert
from kpi.application_kpi import flux_daily_application_by_client
from kpi.client_kpi import count_active_clients_with_recent_payrolls, get_new_clients_by_month
from pymongo import MongoClient
from kpi.doc_kpi import document_average_size_by_type
from kpi.payroll_kpi import count_payroll_by_client_month, taux_fail_payroll_by_client_month

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["database_rh"]
# conversions en list des kpi pour reutilisation CommandCursor(peut etre parcouru une seule fois)
# KPI Clients
kpi_client1 = list(db.clients.aggregate(count_active_clients_with_recent_payrolls(30)))
kpi_client2 = list(db.clients.aggregate(get_new_clients_by_month()))
# KPI Payrolls 
kpi_payroll1 = list(db.payrolls.aggregate(count_payroll_by_client_month()))
kpi_payroll2 = list(db.payrolls.aggregate(taux_fail_payroll_by_client_month()))
# KPI Applications
kpi_application1 = list(db.applications.aggregate(flux_daily_application_by_client()))
# KPI Documents alerts
kpi_alerts = list(db.documents.aggregate(document_average_size_by_type_alert()))

for row in kpi_client1:
    print(f"Clients actifs (30 par défaut): {row['active_clients']}")

for row in kpi_client2:
    print(f"Mois: {row['_id']}, Nouveaux clients: {row['new_clients']}")

for row in kpi_payroll1:
    print(f"Client: {row['clientName']}, Mois: {row['month']}, Nombre de fiches de paie: {row['payroll_count']}")

for row in kpi_payroll2:
    print(f"Jour: {row['day']}, Taux d'échec: {row['taux_echec']:.2f}%")

for row in kpi_application1:
    print(f"Client: {row['clientName']}, Jour: {row['day']}, Nombre d'applications: {row['application_count']}")

for row in kpi_alerts:
    print(f"Type de document: {row['type']}, Taille moyenne: {row['avg_size']:.2f} bytes")

#alerts_threshold = 5.0  # Example threshold for payroll failure rate

payroll_failure_alerts = payroll_failure_alert(kpi_payroll2, threshold=5)
for alert in payroll_failure_alerts:
    print(f"Alerte le {alert['day']}: {alert['alert']} (Valeur: {alert['value']:.2f}%)")

document_size_alerts = document_size_alert(kpi_alerts)
for alert in document_size_alerts:
    print(f"Alerte pour le type {alert['type']}: {alert['alert']} (Taille moyenne: {alert['avg_size']:.2f} bytes)")