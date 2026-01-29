from typing import List, Dict, Any

def payroll_failure_alert(kpi_results: List[Dict[str, Any]], threshold: float = 5.0) -> List[Dict[str, Any]]:
    """
    Génère des alertes pour les fiches de paie lorsque le taux d'échec
    dépasse le seuil spécifié.

    Args:
        kpi_results (List[Dict[str, Any]]): Liste des résultats KPI avec 'failure_rate'.
        threshold (float, optional): Seuil en pourcentage pour déclencher une alerte. Par défaut 5.0.

    Returns:
        List[Dict[str, Any]]: Liste des alertes contenant le jour, le message d'alerte et la valeur.
    """
    alerts = []

    for row in kpi_results:
        # Vérifie que la clé existe et récupère le taux d'échec
        failure_rate = row.get("failure_rate") or row.get("taux_echec", 0)
        if failure_rate > threshold:
            alerts.append({
                "day": row.get("day", "inconnu"),
                "alert": "Le taux d'échec des fiches de paie a dépassé le seuil",
                "value": failure_rate
            })

    return alerts
