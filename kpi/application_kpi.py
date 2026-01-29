from typing import List, Dict, Any


def flux_daily_application_by_client() -> List[Dict[str, Any]]:
    """
    KPI: Daily number of applications per client.
    Groups applications by client and day.
    """
    return [
        {
            "$addFields": {
                "day": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$createdAt",
                    }
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "client_id": "$clientId",
                    "day": "$day",
                },
                "application_count": {"$sum": 1},
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
                "client_name": "$client.name",
                "day": "$_id.day",
                "application_count": 1,
            }
        },
        {
            "$sort": {"day": 1}
        },
    ]
