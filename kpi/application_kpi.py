def flux_daily_application_by_client():
    """
    KPI: Flux quotidien des applications par client
    """
    return [
        {
            "$group": {
                "_id": {
                    "clientId": "$clientId",
                    "day": { "$dateToString": { "format": "%Y-%m-%d", "date": "$createdAt" } }
                },
                "application_count": { "$sum": 1 }
            }
        },
        {
            "$lookup": {
                "from": "clients",
                "localField": "_id.clientId",
                "foreignField": "_id",
                "as": "client"
            }
        },
        {
            "$unwind": "$client"
        },
        {
            "$project": {
                "clientName": "$client.name",
                "day": "$_id.day",
                "application_count": 1
            }
        },
        { "$sort": { "day": 1 } }
    ]