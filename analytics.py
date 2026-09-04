# ==================================================
# SPONSOR PERFORMANCE ANALYTICS
# ==================================================


def calculate_payment_performance(
    contract_value,
    amount_paid
):
    """
    Calculate percentage of sponsorship
    contract that has been paid.
    """

    if not contract_value or contract_value <= 0:
        return 0

    payment_percentage = (
        amount_paid / contract_value
    ) * 100

    return round(
        min(payment_percentage, 100),
        2
    )


# ==================================================
# LEAD PERFORMANCE
# ==================================================

def calculate_lead_performance(
    leads
):
    """
    Convert sponsor leads into a
    normalized performance score.
    """

    if leads is None:
        leads = 0

    # Maximum benchmark = 100 leads
    score = (
        leads / 100
    ) * 100

    return round(
        min(score, 100),
        2
    )


# ==================================================
# ENGAGEMENT PERFORMANCE
# ==================================================

def calculate_engagement_performance(
    engagement_score
):
    """
    Normalize engagement score.
    Expected input range: 0-100
    """

    if engagement_score is None:
        engagement_score = 0

    return round(
        max(
            0,
            min(
                engagement_score,
                100
            )
        ),
        2
    )


# ==================================================
# OVERALL PERFORMANCE SCORE
# ==================================================

def calculate_overall_score(
    payment_performance,
    lead_performance,
    engagement_performance
):
    """
    Weighted sponsor performance score.

    Payment       = 40%
    Leads         = 30%
    Engagement    = 30%
    """

    overall_score = (

        payment_performance * 0.40

        +

        lead_performance * 0.30

        +

        engagement_performance * 0.30

    )

    return round(
        overall_score,
        2
    )


# ==================================================
# SPONSOR HEALTH
# ==================================================

def determine_sponsor_health(
    overall_score
):
    """
    Determine sponsor health
    based on overall performance.
    """

    if overall_score >= 80:

        return "Excellent"

    elif overall_score >= 65:

        return "Good"

    elif overall_score >= 50:

        return "Needs Attention"

    else:

        return "At Risk"


# ==================================================
# AI RECOMMENDATION
# ==================================================

def generate_sponsor_recommendation(
    sponsor,
    payment_performance,
    lead_performance,
    engagement_performance,
    overall_score,
    health
):
    """
    Generate rule-based AI-style
    recommendations for sponsor management.
    """

    recommendations = []


    # ----------------------------------------------
    # PAYMENT RECOMMENDATION
    # ----------------------------------------------

    if payment_performance < 50:

        recommendations.append(
            "Follow up with the sponsor regarding "
            "pending contract payment."
        )

    elif payment_performance < 80:

        recommendations.append(
            "Monitor the remaining sponsorship "
            "payment and schedule a follow-up."
        )

    else:

        recommendations.append(
            "Sponsor payment performance is healthy."
        )


    # ----------------------------------------------
    # LEAD RECOMMENDATION
    # ----------------------------------------------

    if lead_performance < 40:

        recommendations.append(
            "Increase sponsor visibility and "
            "lead-generation activities."
        )

    elif lead_performance < 70:

        recommendations.append(
            "Improve lead-generation opportunities "
            "through targeted event engagement."
        )

    else:

        recommendations.append(
            "Sponsor is generating strong lead activity."
        )


    # ----------------------------------------------
    # ENGAGEMENT RECOMMENDATION
    # ----------------------------------------------

    if engagement_performance < 40:

        recommendations.append(
            "Increase sponsor engagement through "
            "sessions, booths and networking activities."
        )

    elif engagement_performance < 70:

        recommendations.append(
            "Improve sponsor engagement with "
            "interactive event activities."
        )

    else:

        recommendations.append(
            "Sponsor engagement is performing well."
        )


    # ----------------------------------------------
    # OVERALL RECOMMENDATION
    # ----------------------------------------------

    if health == "Excellent":

        overall_recommendation = (
            "Maintain the current sponsorship strategy "
            "and consider long-term partnership opportunities."
        )

    elif health == "Good":

        overall_recommendation = (
            "Sponsor performance is positive. "
            "Focus on improving weaker performance areas."
        )

    elif health == "Needs Attention":

        overall_recommendation = (
            "Sponsor requires additional attention. "
            "Review payment, leads and engagement performance."
        )

    else:

        overall_recommendation = (
            "Sponsor is at risk. "
            "Immediate account review and corrective "
            "actions are recommended."
        )


    return {

        "overall_recommendation":
            overall_recommendation,

        "action_items":
            recommendations

    }


# ==================================================
# COMPLETE SPONSOR ANALYTICS
# ==================================================

def analyze_sponsor_performance(
    sponsor
):
    """
    Generate complete sponsor performance analytics.
    """

    # ----------------------------------------------
    # RAW DATA
    # ----------------------------------------------

    contract_value = (
        sponsor.contract_value or 0
    )

    amount_paid = (
        sponsor.amount_paid or 0
    )

    leads = (
        sponsor.leads or 0
    )

    engagement_score = (
        sponsor.engagement_score or 0
    )


    # ----------------------------------------------
    # PERFORMANCE CALCULATIONS
    # ----------------------------------------------

    payment_performance = (
        calculate_payment_performance(

            contract_value,

            amount_paid

        )
    )


    lead_performance = (
        calculate_lead_performance(

            leads

        )
    )


    engagement_performance = (
        calculate_engagement_performance(

            engagement_score

        )
    )


    # ----------------------------------------------
    # OVERALL SCORE
    # ----------------------------------------------

    overall_score = (
        calculate_overall_score(

            payment_performance,

            lead_performance,

            engagement_performance

        )
    )


    # ----------------------------------------------
    # HEALTH
    # ----------------------------------------------

    health = (
        determine_sponsor_health(
            overall_score
        )
    )


    # ----------------------------------------------
    # AI RECOMMENDATION
    # ----------------------------------------------

    recommendation = (
        generate_sponsor_recommendation(

            sponsor,

            payment_performance,

            lead_performance,

            engagement_performance,

            overall_score,

            health

        )
    )


    # ----------------------------------------------
    # FINAL ANALYTICS RESULT
    # ----------------------------------------------

    return {

        "sponsor_id":
            sponsor.id,

        "sponsor_name":
            sponsor.name,

        "sponsor_tier":
            sponsor.tier,

        "financial_metrics": {

            "contract_value":
                contract_value,

            "amount_paid":
                amount_paid,

            "payment_percentage":
                payment_performance

        },

        "performance_metrics": {

            "leads":
                leads,

            "lead_performance":
                lead_performance,

            "engagement_score":
                engagement_score,

            "engagement_performance":
                engagement_performance

        },

        "analytics": {

            "overall_score":
                overall_score,

            "health":
                health

        },

        "ai_recommendation":
            recommendation

    }