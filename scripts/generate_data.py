
import random
from datetime import datetime
from faker import Faker
from pymongo import MongoClient

fake = Faker()

client = MongoClient("mongodb+srv://gueyebamba39_db_user:vkPGrrKq2EsdaS5h@cluster0.1m4tyvi.mongodb.net/")
db = client["database_rh"]

# Nettoyage
db.clients.delete_many({})
db.employees.delete_many({})
db.payrolls.delete_many({})
db.payroll_reports.delete_many({})
db.applications.delete_many({})
db.documents.delete_many({})

# --------------------
# CLIENTS
# --------------------
clients = []
for _ in range(10):
    clients.append({
        "name": fake.company(),
        "status": random.choice(["active", "inactive"]),
        "createdAt": fake.date_time_this_year()
    })

client_ids = db.clients.insert_many(clients).inserted_ids

# --------------------
# EMPLOYEES
# --------------------
employees = []
for cid in client_ids:
    for _ in range(random.randint(5, 15)):
        employees.append({
            "clientId": cid,
            "name": fake.name(),
            "status": "active",
            "createdAt": fake.date_time_this_year()
        })

employee_ids = db.employees.insert_many(employees).inserted_ids

# --------------------
# PAYROLLS (FICHES DE PAIE)
# --------------------
payrolls = []
for emp in db.employees.find():
    payrolls.append({
        "clientId": emp["clientId"],
        "employeeId": emp["_id"],
        "month": "2026-01",
        "netSalary": random.randint(150000, 900000),
        "status": random.choices(
            ["success", "failed"], weights=[90, 10]
        )[0],
        "createdAt": datetime.utcnow()
    })

db.payrolls.insert_many(payrolls)

# --------------------
# PAYROLL REPORTS (ETATS DE PAIE)
# --------------------
for cid in client_ids:
    employee_count = db.employees.count_documents({"clientId": cid})
    total_net = sum(
        p["netSalary"]
        for p in db.payrolls.find({"clientId": cid, "status": "success"})
    )

    db.payroll_reports.insert_one({
        "clientId": cid,
        "month": "2026-01",
        "totalEmployees": employee_count,
        "totalNet": total_net,
        "createdAt": datetime.utcnow()
    })

# --------------------
# APPLICATIONS (RECRUTEMENT)
# --------------------
applications = []
for cid in client_ids:
    for _ in range(random.randint(5, 20)):
        applications.append({
            "clientId": cid,
            "status": random.choice(
                ["pending", "processed", "rejected", "hired"]
            ),
            "createdAt": fake.date_time_this_year()
        })

db.applications.insert_many(applications)

# --------------------
# DOCUMENTS
# --------------------
documents = []
for cid in client_ids:
    for _ in range(random.randint(5, 15)):
        documents.append({
            "clientId": cid,
            "type": random.choice(["contract", "payslip", "certificate"]),
            "generated": random.choice([True, False]),
            "createdAt": fake.date_time_this_year()
        })

db.documents.insert_many(documents)

print("✅ Données générées avec succès")
