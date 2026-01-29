



def count_payroll_by_client_month():

    """
     KPI: Nombre de fiches de paie générées par client / par mois

    """
    return [

        # Ajouter le champ month (YYYY-MM)
        {
            "$addFields": {
            "month": {
                "$dateToString": { "format": "%Y-%m", "date": "$createdAt" }
            }
            }
        },

        # Grouper par client + mois
        {
            "$group": {
            "_id": {
                "clientId": "$clientId",
                "month": "$month"
            },
            "payroll_count": { "$sum": 1 }
            }
        },

        #  Lookup pour le nom du client
        {
            "$lookup": {
            "from": "clients",
            "localField": "_id.clientId",
            "foreignField": "_id",
            "as": "client"
            }
        },
        { "$unwind": "$client" },
        # Projection propre
        {
            "$project": {
            "_id": 0,
            "clientId": "$_id.clientId",
            "clientName": "$client.name",
            "month": "$_id.month",
            "payroll_count": 1
            }
        },

        # Tri chronologique
        { "$sort": { "month": 1 } }
    ]

def taux_fail_payroll_by_client_month():
    """
    KPI: Taux d'échec de fiches de paie par jour
    """
    return [
            {
                "$group": {
                "_id": "$day",
                "total": { "$sum": 1 },
                "failed": {
                    "$sum": {
                    "$cond": [{ "$eq": ["$status", "failed"] }, 1, 0]
                    }
                }
                }
            },
            {
                "$project": {
                "day": "$_id",
                "taux_echec": {
                    "$multiply": [
                    { "$divide": ["$failed", "$total"] },
                    100
                    ]
                }
                }
            },
            { "$sort": { "day": 1 } }
        ]

             

             

             

             

             

             

             

             

             

             

             

             

             

             

             

             

             

             

              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


              


               