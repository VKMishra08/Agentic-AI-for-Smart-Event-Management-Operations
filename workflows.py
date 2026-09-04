from datetime import datetime

from agents import incident_agent

from alert_engine import (
    generate_incident_alert
)


# ==================================================
# INCIDENT MANAGEMENT WORKFLOW
# ==================================================

def execute_incident_workflow(
    db,
    incident
):

    # ----------------------------------------------
    # STEP 1
    # Run Incident Agent
    # ----------------------------------------------

    analysis = incident_agent(
        incident
    )


    # ----------------------------------------------
    # STEP 2
    # Update Priority
    # ----------------------------------------------

    incident.priority = (
        analysis["priority"]
    )


    # ----------------------------------------------
    # STEP 3
    # Update Escalation
    # ----------------------------------------------

    incident.escalation_level = (
        analysis["escalation_level"]
    )


    # ----------------------------------------------
    # STEP 4
    # Automatic Status
    # ----------------------------------------------

    if analysis["priority"] in [

        "Critical",
        "High"

    ]:

        incident.status = "Escalated"


    elif analysis["priority"] == "Medium":

        incident.status = "In Progress"


    else:

        incident.status = "Open"


    # ----------------------------------------------
    # STEP 5
    # Update Timestamp
    # ----------------------------------------------

    incident.updated_at = (
        datetime.utcnow()
    )


    # ----------------------------------------------
    # STEP 6
    # Save Incident
    # ----------------------------------------------

    db.commit()

    db.refresh(incident)


    # ----------------------------------------------
    # STEP 7
    # GENERATE OPERATIONAL ALERT
    # ----------------------------------------------

    alert_result = (
        generate_incident_alert(

            db,

            incident,

            analysis

        )
    )


    # ----------------------------------------------
    # FINAL WORKFLOW RESULT
    # ----------------------------------------------

    return {

        "success": True,

        "workflow":
            "Incident Management Workflow",

        "incident_id":
            incident.id,

        "priority":
            analysis["priority"],

        "risk_score":
            analysis["risk_score"],

        "escalation_level":
            analysis["escalation_level"],

        "status":
            incident.status,

        "response_team":
            analysis["response_team"],

        "recommended_action":
            analysis["recommended_action"],

        "alert":
            alert_result

    }