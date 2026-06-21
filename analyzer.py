"""Generate rule-based and AI-assisted phishing analysis explanations."""

import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def generate_analysis(indicator_results, risk_results):
    """Create a plain-English security explanation from analysis results.

    Args:
        indicator_results: Results returned by detect_phishing_indicators().
        risk_results: Results returned by calculate_risk_score().

    Returns:
        A detailed security explanation as a string.
    """
    indicators_found = indicator_results["indicators_found"]
    risk_level = risk_results["risk_level"]

    # Build the first sentence based on whether any indicators were detected.
    if indicators_found:
        indicator_text = ", ".join(indicators_found)
        reason = (
            "This email appears suspicious because the following indicators "
            f"were detected: {indicator_text}."
        )
    else:
        reason = "No obvious phishing indicators were detected in this email."

    # Explain the overall risk level from the scoring engine.
    risk_explanation = f"The overall risk level is {risk_level}."

    # Provide a simple recommendation based on the risk level.
    if risk_level == "High":
        recommendation = (
            "Users should avoid clicking links, opening attachments, or "
            "submitting credentials until the sender has been independently "
            "verified."
        )
    elif risk_level == "Medium":
        recommendation = (
            "Users should review the message carefully and verify the sender "
            "through a trusted channel before taking action."
        )
    else:
        recommendation = (
            "Users should still remain cautious and confirm unexpected requests "
            "before sharing sensitive information."
        )

    return f"{reason} {risk_explanation} {recommendation}"


def generate_ai_analysis(email_text, indicator_results, risk_results):
    """Generate a concise AI-assisted phishing analysis explanation.

    If the OpenAI API key is missing or the API request fails, this function
    returns the existing rule-based explanation instead.

    Args:
        email_text: The original email content as a string.
        indicator_results: Results returned by detect_phishing_indicators().
        risk_results: Results returned by calculate_risk_score().

    Returns:
        A concise security explanation as a string.
    """
    # Load variables from a local .env file, including OPENAI_API_KEY.
    if load_dotenv is not None:
        load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    # Temporary debugging message. This can later be changed back to a graceful fallback.
    if OpenAI is None:
        return "OPENAI ERROR: OpenAI package is not installed."

    # Temporary debugging message. This can later be changed back to a graceful fallback.
    if not api_key:
        return "OPENAI ERROR: API key not found in .env file."

    # Collect the important analysis details for the model prompt.
    indicators_found = indicator_results["indicators_found"]
    risk_level = risk_results["risk_level"]
    risk_score = risk_results["score"]

    prompt = f"""
Analyze this email for phishing risk.

Original email:
{email_text}

Detected indicators:
{indicators_found}

Risk level:
{risk_level}

Risk score:
{risk_score}/3

Explain why the email may be phishing, explain the detected indicators,
and provide a security recommendation. Keep the response concise, about
1-2 paragraphs.
"""

    try:
        # Create an OpenAI client with the API key from the environment.
        client = OpenAI(api_key=api_key)

        # Ask the model for a concise security explanation.
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )

        return response.output_text
    except Exception as e:
        # Temporary debugging message. This can later be changed back to a graceful fallback.
        return f"OPENAI ERROR: {str(e)}"
