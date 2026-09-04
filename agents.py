# ==================================================
# AI AGENTS
# Sponsorship & Incident Management
# ==================================================


# ==================================================
# SPONSORSHIP AGENT
# ==================================================

def sponsorship_agent(sponsor):

    # ----------------------------------------------
    # Payment Performance
    # ----------------------------------------------

    if sponsor.contract_value and sponsor.contract_value > 0:

        payment_ratio = (
            sponsor.amount_paid
            / sponsor.contract_value
        ) * 100

    else:

        payment_ratio = 0


    # ----------------------------------------------
    # Lead Performance
    # ----------------------------------------------

    leads = sponsor.leads or 0

    lead_score = min(
        leads / 5,
        100
    )


    # ----------------------------------------------
    # Engagement
    # ----------------------------------------------

    engagement_score = (
        sponsor.engagement_score or 0
    )


    # ----------------------------------------------
    # Overall Performance Score
    # ----------------------------------------------

    performance_score = (

        engagement_score * 0.45

        +

        lead_score * 0.30

        +

        min(payment_ratio, 100) * 0.25

    )


    performance_score = round(
        min(performance_score, 100),
        2
    )


    # ----------------------------------------------
    # Sponsor Health
    # ----------------------------------------------

    if performance_score >= 80:

        health = "Excellent"

        recommendation = (
            "Sponsor is performing very well. "
            "Consider contract renewal and "
            "premium visibility opportunities."
        )


    elif performance_score >= 60:

        health = "Good"

        recommendation = (
            "Sponsor performance is stable. "
            "Increase engagement activities and "
            "lead-generation opportunities."
        )


    elif performance_score >= 40:

        health = "Needs Attention"

        recommendation = (
            "Sponsor engagement is below target. "
            "Increase promotional activities, "
            "booth engagement and communication."
        )


    else:

        health = "At Risk"

        recommendation = (
            "Sponsor requires immediate attention. "
            "Schedule a sponsor review and create "
            "a performance recovery plan."
        )


    # ----------------------------------------------
    # Action Items
    # ----------------------------------------------

    action_items = []


    if payment_ratio < 50:

        action_items.append(
            "Follow up with sponsor regarding pending payment."
        )


    if lead_score < 50:

        action_items.append(
            "Increase sponsor lead-generation activities."
        )


    if engagement_score < 50:

        action_items.append(
            "Increase sponsor engagement and communication."
        )


    if performance_score >= 80:

        action_items.append(
            "Consider sponsor renewal and premium visibility."
        )


    if not action_items:

        action_items.append(
            "Continue monitoring sponsor performance."
        )


    # ----------------------------------------------
    # Agent Result
    # ----------------------------------------------

    return {

        "sponsor_id":
            sponsor.id,

        "sponsor_name":
            sponsor.name,

        "performance_score":
            performance_score,

        "health":
            health,

        "payment_ratio":
            round(
                payment_ratio,
                2
            ),

        "lead_score":
            round(
                lead_score,
                2
            ),

        "engagement_score":
            engagement_score,

        "recommendation":
            recommendation,

        "action_items":
            action_items

    }


# ==================================================
# INCIDENT AGENT
# ==================================================

def incident_agent(incident):

    # ----------------------------------------------
    # Severity Weights
    # ----------------------------------------------

    severity_weights = {

        "Low": 1,

        "Medium": 2,

        "High": 3,

        "Critical": 4

    }


    # Normalize severity
    severity = (
        incident.severity or "Medium"
    )


    severity_weight = (
        severity_weights.get(
            severity,
            2
        )
    )


    # ----------------------------------------------
    # Impact Calculation
    # ----------------------------------------------

    affected_people = (
        incident.affected_people or 0
    )


    impact_score = min(
        affected_people,
        100
    )


    # ----------------------------------------------
    # RISK SCORE
    # ----------------------------------------------

    risk_score = (

        severity_weight * 20

        +

        impact_score * 0.4

    )


    risk_score = round(
        min(
            risk_score,
            100
        ),
        2
    )


    # ==================================================
    # PRIORITY + ESCALATION
    # ==================================================

    if (

        severity == "Critical"

        or

        affected_people >= 100

        or

        risk_score >= 80

    ):

        priority = "Critical"

        escalation_level = 3

        escalation_status = "Immediate Escalation"

        recommended_action = (
            "Immediately escalate to event leadership, "
            "activate emergency response and assign "
            "a dedicated incident commander."
        )


    elif (

        severity == "High"

        or

        affected_people >= 50

        or

        risk_score >= 60

    ):

        priority = "High"

        escalation_level = 2

        escalation_status = "Escalate to Operations Lead"

        recommended_action = (
            "Assign an incident owner immediately, "
            "notify the operations lead and monitor "
            "the incident continuously."
        )


    elif (

        severity == "Medium"

        or

        affected_people >= 10

        or

        risk_score >= 40

    ):

        priority = "Medium"

        escalation_level = 1

        escalation_status = "Operations Team Monitoring"

        recommended_action = (
            "Assign the incident to the operations team "
            "and monitor it until resolution."
        )


    else:

        priority = "Low"

        escalation_level = 0

        escalation_status = "Standard Operations"

        recommended_action = (
            "Add the incident to the standard operations "
            "queue and resolve through normal procedures."
        )


    # ==================================================
    # RESPONSE TEAM
    # ==================================================

    category = (
        incident.category or ""
    )


    if category == "Technical":

        response_team = (
            "Technical Operations Team"
        )


    elif category == "Speaker":

        response_team = (
            "Speaker Management Team"
        )


    elif category == "Venue":

        response_team = (
            "Venue Operations Team"
        )


    elif category == "Registration":

        response_team = (
            "Registration Team"
        )


    else:

        response_team = (
            "Event Operations Team"
        )


    # ==================================================
    # INCIDENT STATUS
    # ==================================================

    incident_status = getattr(
        incident,
        "status",
        None
    )


    if not incident_status:

        incident_status = "Open"


    # ==================================================
    # AI RECOMMENDATION
    # ==================================================

    if priority == "Critical":

        ai_recommendation = (
            "Critical incident detected. "
            "Immediate escalation and emergency "
            "response are required."
        )


    elif priority == "High":

        ai_recommendation = (
            "High-priority incident detected. "
            "Assign an incident owner and escalate "
            "to the operations lead."
        )


    elif priority == "Medium":

        ai_recommendation = (
            "Medium-priority incident detected. "
            "Continue operational monitoring and "
            "resolve through the assigned team."
        )


    else:

        ai_recommendation = (
            "Low-priority incident detected. "
            "Handle through standard operational procedures."
        )


    # ==================================================
    # FINAL INCIDENT AGENT RESPONSE
    # ==================================================

    return {

        "incident_id":
            incident.id,

        "incident_title":
            incident.title,

        "severity":
            severity,

        "priority":
            priority,

        "risk_score":
            risk_score,

        "affected_people":
            affected_people,

        "escalation_level":
            escalation_level,

        "escalation_status":
            escalation_status,

        "response_team":
            response_team,

        "status":
            incident_status,

        "recommended_action":
            recommended_action,

        "ai_recommendation":
            ai_recommendation

    }