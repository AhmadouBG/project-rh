from typing import List, Dict, Any


def document_average_size_by_type() -> List[Dict[str, Any]]:
    """
    MongoDB aggregation pipeline qui calcule
    la taille moyenne des documents par type.
    """
    return [
        {
            "$group": {
                "_id": "$type",
                "avg_size": {"$avg": "$file.size_bytes"},
            }
        }
    ]
