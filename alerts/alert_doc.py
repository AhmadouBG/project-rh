from typing import List, Dict, Any

# =========================
# Constants (no magic numbers)
# =========================

DOCUMENT_SIZE_THRESHOLDS = {
    "certificate": 2500 * 2,
    "payslip": 120_000 * 2,
    "contract": 600_000 * 2,
}


# =========================
# MongoDB Aggregation Pipeline
# =========================

def document_average_size_by_type_alert() -> List[Dict[str, Any]]:
    """
    MongoDB aggregation pipeline that detects
    abnormal average document sizes per day and type.
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
                    "day": "$day",
                    "type": "$type",
                },
                "avg_size": {"$avg": "$file.size_bytes"},
            }
        },
        {
            "$match": {
                "$expr": {
                    "$or": [
                        {
                            "$and": [
                                {"$eq": ["$_id.type", "certificate"]},
                                {"$gt": ["$avg_size", DOCUMENT_SIZE_THRESHOLDS["certificate"]]},
                            ]
                        },
                        {
                            "$and": [
                                {"$eq": ["$_id.type", "payslip"]},
                                {"$gt": ["$avg_size", DOCUMENT_SIZE_THRESHOLDS["payslip"]]},
                            ]
                        },
                        {
                            "$and": [
                                {"$eq": ["$_id.type", "contract"]},
                                {"$gt": ["$avg_size", DOCUMENT_SIZE_THRESHOLDS["contract"]]},
                            ]
                        },
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "day": "$_id.day",
                "type": "$_id.type",
                "avg_size": 1,
            }
        },
        {
            "$sort": {"day": 1}
        },
    ]


# =========================
# Alert Formatter
# =========================

def document_size_alert(kpi_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converts KPI results into alert objects.
    """
    alerts = []

    for row in kpi_results:
        alerts.append(
            {
                "day": row["day"],
                "type": row["type"],
                "alert": "La taille moyenne des documents a dépassé le seuil autorisé.",
                "avg_size": row["avg_size"],
            }
        )

    return alerts
