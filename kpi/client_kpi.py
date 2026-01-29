from datetime import datetime, timedelta
from typing import List, Dict, Any


def count_active_clients_with_recent_payrolls(
    days: int = 30,
) -> List[Dict[str, Any]]:
    """
    KPI: Nombre de clients actifs ayant généré au moins une paie
    au cours des `days` derniers jours (par défaut : 30).
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    return [
        {
            "$match": {
                "status": "active",
            }
        },
        {
            "$lookup": {
                "from": "payrolls",
                "localField": "_id",
                "foreignField": "clientId",
                "as": "payrolls",
            }
        },
        {
            "$match": {
                "payrolls": {
                    "$elemMatch": {
                        "createdAt": {
                            "$gte": start_date,
                        }
                    }
                }
            }
        },
        {
            "$count": "active_clients",
        },
    ]


def get_new_clients_by_month() -> List[Dict[str, Any]]:
    """
    KPI: Numbre de nouveaux clients par mois.
    """
    return [
        {
            "$addFields": {
                "month": {
                    "$dateToString": {
                        "format": "%Y-%m",
                        "date": "$createdAt",
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$month",
                "new_clients": {"$sum": 1},
            }
        },
        {
            "$sort": {"_id": 1},
        },
    ]
