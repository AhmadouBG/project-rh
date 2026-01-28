from datetime import datetime, timedelta

def count_active_clients_with_recent_payrolls(days=30):
    """
    KPI: Nombre de clients actifs ayant généré au moins un payroll
    sur les X derniers jours (30 par défaut)
    """

    start_date = datetime.utcnow() - timedelta(days=days)

    return [
        {
            "$match": {
                "status": "active"
            }
        },
        {
            "$lookup": {
                "from": "payrolls",
                "localField": "_id",
                "foreignField": "clientId",
                "as": "payrolls"
            }
        },
        {
            "$match": {
                "payrolls": {
                    "$elemMatch": {
                        "createdAt": {
                            "$gte": start_date
                        }
                    }
                }
            }
        },
        {
            "$count": "active_clients"
        }
    ]



def get_new_clients_by_month(db):
    """
    KPI: Nombre de nouveaux clients par mois
    """
    return [
        # Extraire le mois de création
        {
            "$addFields": {
                "month": {
                    "$dateToString": { "format": "%Y-%m", "date": "$createdAt" }
                }
            }
        },
        # Grouper par mois et compter les clients
        {
            "$group": {
                "_id": "$month",
                "new_clients": { "$sum": 1 }
            }
        },
        # Trier chronologiquement
        { "$sort": { "_id": 1 } }
    ]
