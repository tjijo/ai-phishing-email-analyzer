"""Streamlit app for the AI Phishing Email Analyzer."""

import streamlit as st

from analyzer import generate_ai_analysis
from risk_scoring import calculate_risk_score
from utils.indicators import detect_phishing_indicators


# Page setup
st.set_page_config(page_title="AI Phishing Email Analyzer")


# App header and description
st.title("AI Phishing Email Analyzer")
st.write(
    "Paste an email below to check it for common phishing signals. "
    "This early version sets up the interface before analysis features are added."
)


# Email input area
email_content = st.text_area(
    "Email content",
    placeholder="Paste the full email message here...",
    height=300,
)


# Analyze button and basic validation
if st.button("Analyze Email"):
    if not email_content.strip():
        st.warning("Please paste email content before analyzing.")
    else:
        # Run the phishing indicator engine on the pasted email text.
        analysis_result = detect_phishing_indicators(email_content)
        indicators_found = analysis_result["indicators_found"]

        # Calculate the risk score based on the detected indicators.
        risk_result = calculate_risk_score(analysis_result)
        risk_level = risk_result["risk_level"]
        risk_score = risk_result["score"]

        # Generate an AI-assisted explanation of the analysis results.
        analysis_explanation = generate_ai_analysis(
            email_content,
            analysis_result,
            risk_result,
        )

        # Display the risk level with simple color-coded Streamlit messages.
        st.subheader("Risk Level")

        if risk_level == "High":
            st.error(f"Risk Level: {risk_level}")
        elif risk_level == "Medium":
            st.warning(f"Risk Level: {risk_level}")
        else:
            st.success(f"Risk Level: {risk_level}")

        # Display the numeric score after the risk level.
        st.write(f"Risk Score: {risk_score}/3")

        # Display the generated security explanation.
        st.subheader("AI Security Assessment")
        st.write(analysis_explanation)

        # Display the detected indicators in a simple, readable format.
        st.subheader("Indicators Found")

        if indicators_found:
            for indicator in indicators_found:
                st.write(f"- {indicator}")
        else:
            st.success("No phishing indicators detected.")
