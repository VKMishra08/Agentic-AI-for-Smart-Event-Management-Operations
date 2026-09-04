from models import Alert


# ==================================================
# OPERATIONAL ALERT ENGINE
# ==================================================

def generate_incident_alert(
    db,
    incident,
    analysis
):

    priority = analysis["priority"]
    risk_score = analysis["risk_score"]

    # ----------------------------------------------
    # Critical Alert
    # ----------------------------------------------

    if priority == "Critical":

        alert_level = "CRITICAL"

        title = (
            f"Critical Incident: "
            f"{incident.title}"
        )

        message = (
            f"Critical incident detected. "
            f"Risk score: {risk_score}. "
            f"Immediate escalation is required. "
            f"Escalation Level: "
            f"{analysis['escalation_level']}."
        )


    # ----------------------------------------------
    # High Priority Alert
    # ----------------------------------------------

    elif priority == "High":

        alert_level = "HIGH"

        title = (
            f"High Priority Incident: "
            f"{incident.title}"
        )

        message = (
            f"High priority incident requires "
            f"immediate operational attention. "
            f"Risk score: {risk_score}. "
            f"Response Team: "
            f"{analysis['response_team']}."
        )


    # ----------------------------------------------
    # Medium Alert
    # ----------------------------------------------

    elif priority == "Medium":

        alert_level = "MEDIUM"

        title = (
            f"Incident Monitoring: "
            f"{incident.title}"
        )

        message = (
            f"Medium priority incident detected. "
            f"Continue monitoring and resolve "
            f"through the assigned operations team."
        )


    # ----------------------------------------------
    # Information Alert
    # ----------------------------------------------

    else:

        alert_level = "INFO"

        title = (
            f"Operational Information: "
            f"{incident.title}"
        )

        message = (
            f"Low priority incident recorded "
            f"for operational monitoring."
        )


    # ----------------------------------------------
    # Create Alert
    # ----------------------------------------------

    alert = Alert(

        title=title,

        message=message,

        level=alert_level,

        source="Incident Agent",

        resolved=0

    )


    db.add(alert)

    db.commit()

    db.refresh(alert)


    return {

        "success": True,

        "alert_id": alert.id,

        "level": alert.level,

        "title": alert.title,

        "message": alert.message,

        "source": alert.source,

        "resolved": bool(
            alert.resolved
        )

    }