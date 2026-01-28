from kpi.application_kpi import flux_daily_application_by_client
from kpi.client_kpi import count_active_clients_with_recent_payrolls, get_new_clients_by_month
from pymongo import MongoClient
from kpi.payroll_kpi import count_payroll_by_client_month, taux_fail_payroll_by_client_month

client = MongoClient("mongodb://localhost:27017")
db = client["database_rh"]

kpi_client1 = db.clients.aggregate(count_active_clients_with_recent_payrolls(30))
kpi_client2 = db.clients.aggregate(get_new_clients_by_month())

kpi_payroll1 = db.payrolls.aggregate(count_payroll_by_client_month())
kpi_payroll2 = db.payrolls.aggregate(taux_fail_payroll_by_client_month())

kpi_application1 = db.applications.aggregate(flux_daily_application_by_client())

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
