from typing import List, Dict, Any


def count_payroll_by_client_month() -> List[Dict[str, Any]]:
    """
    KPI: Nombre de paies générées par client par mois.
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
                "_id": {
                    "client_id": "$clientId",
                    "month": "$month",
                },
                "payroll_count": {"$sum": 1},
            }
        },
        {
            "$lookup": {
                "from": "clients",
                "localField": "_id.client_id",
                "foreignField": "_id",
                "as": "client",
            }
        },
        {
            "$unwind": "$client"
        },
        {
            "$project": {
                "_id": 0,
                "client_id": "$_id.client_id",
                "client_name": "$client.name",
                "month": "$_id.month",
                "payroll_count": 1,
            }
        },
        {
            "$sort": {"month": 1}
        },
    ]


def failure_rate_payroll_by_client_month() -> List[Dict[str, Any]]:
    """
    KPI: Taux d'échec de la paie par client et par mois.
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
                "_id": {
                    "client_id": "$clientId",
                    "month": "$month",
                },
                "total": {"$sum": 1},
                "failed": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$status", "failed"]},
                            1,
                            0,
                        ]
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "client_id": "$_id.client_id",
                "month": "$_id.month",
                "failure_rate": {
                    "$multiply": [
                        {"$divide": ["$failed", "$total"]},
                        100,
                    ]
                },
            }
        },
        {
            "$sort": {"month": 1}
        },
    ]


             

             

             

             

             

             

             

             

             

             

             

             

             

             

             

             

             

              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


               