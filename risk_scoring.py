"""Calculate phishing risk scores from detected email indicators."""


def calculate_risk_score(indicator_results):
    """Calculate a simple risk score and risk level from indicator results.

    Args:
        indicator_results: A dictionary returned by detect_phishing_indicators.

    Returns:
        A dictionary containing the numeric score and matching risk level.
    """
    # These are the boolean flags that count toward the final risk score.
    detection_flags = [
        indicator_results["urgency_detected"],
        indicator_results["credential_request_detected"],
        indicator_results["suspicious_link_detected"],
    ]

    # In Python, True counts as 1 and False counts as 0.
    score = sum(detection_flags)

    # Convert the numeric score into an easy-to-understand risk level.
    if score <= 1:
        risk_level = "Low"
    elif score == 2:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "score": score,
        "risk_level": risk_level,
    }
