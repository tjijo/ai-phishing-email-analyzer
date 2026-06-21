"""Detect simple phishing indicators in email text."""


# Words and phrases that often appear in urgent phishing emails.
URGENCY_KEYWORDS = [
    "urgent",
    "immediately",
    "act now",
    "limited time",
    "expires today",
    "final notice",
    "account suspended",
]


# Words and phrases that ask users to reveal private account information.
CREDENTIAL_REQUEST_KEYWORDS = [
    "password",
    "login",
    "verify your account",
    "confirm your account",
    "update your account",
    "security code",
    "credentials",
]


# Simple link patterns that can be suspicious in beginner-level detection.
SUSPICIOUS_LINK_KEYWORDS = [
    "http://",
    "bit.ly",
    "tinyurl",
    "click here",
    "login.",
    "verify.",
]


def detect_phishing_indicators(email_text):
    """Check email text for basic phishing indicators using keyword matching.

    Args:
        email_text: The full email content as a string.

    Returns:
        A dictionary with boolean detection flags and a list of indicators found.
    """
    # Normalize the text once so matching is case-insensitive.
    normalized_text = email_text.lower()

    indicators_found = []

    # Check for urgency language.
    urgency_detected = any(
        keyword in normalized_text for keyword in URGENCY_KEYWORDS
    )
    if urgency_detected:
        indicators_found.append("Urgency language detected")

    # Check for requests related to passwords, logins, or account verification.
    credential_request_detected = any(
        keyword in normalized_text for keyword in CREDENTIAL_REQUEST_KEYWORDS
    )
    if credential_request_detected:
        indicators_found.append("Credential request language detected")

    # Check for simple suspicious link patterns.
    suspicious_link_detected = any(
        keyword in normalized_text for keyword in SUSPICIOUS_LINK_KEYWORDS
    )
    if suspicious_link_detected:
        indicators_found.append("Suspicious link detected")

    return {
        "urgency_detected": urgency_detected,
        "credential_request_detected": credential_request_detected,
        "suspicious_link_detected": suspicious_link_detected,
        "indicators_found": indicators_found,
    }
