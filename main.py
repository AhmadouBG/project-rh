from kpi.client_kpi import count_active_clients_with_recent_payrolls, get_new_clients_by_month
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["database_rh"]

kpi_client1 = db.clients.aggregate(count_active_clients_with_recent_payrolls(30))
kpi_client2 = db.clients.aggregate(get_new_clients_by_month())
print("KPI: Nombre de clients actifs avec des fiches de paie récentes")

for row in kpi_client1:
    print(f"Clients actifs (30 par défaut): {row['active_clients']}")

for row in kpi_client2:
    print(f"Mois: {row['_id']}, Nouveaux clients: {row['new_clients']}")



