# app.py

import streamlit as st
import config

import gpt_provider
import time



# Example dummy match data (replace with API later)
matches = [
    {
        "team_a": "Manchester United",
        "team_b": "Liverpool",
        "team_a_form": "W-W-D-L",
        "team_b_form": "L-W-L-W",
        "team_a_injuries": "None",
        "team_b_injuries": "Star striker out",
        "odds": "Man U win 1.8, Draw 3.5, Liverpool win 4.2"
    },
    {
        "team_a": "Real Madrid",
        "team_b": "Barcelona",
        "team_a_form": "W-W-W-W",
        "team_b_form": "D-W-L-W",
        "team_a_injuries": "Defender missing",
        "team_b_injuries": "No key injuries",
        "odds": "Real Madrid win 2.0, Draw 3.0, Barcelona win 3.5"
    }
]

# Streamlit App
st.set_page_config(page_title="AI Sports Betting Helper", page_icon="⚽")
st.title("⚽ AI Sports Betting Helper")
st.markdown(f"### Select a match to get AI-powered prediction (using **{gpt_provider.OPENAI_MODEL}**)")

# Display matches as buttons
for match in matches:
    if st.button(f"{match['team_a']} vs {match['team_b']}"):
        st.subheader("Match Details")
        st.write(f"**Form:** {match['team_a']} ({match['team_a_form']}) vs {match['team_b']} ({match['team_b_form']})")
        st.write(
            f"**Injuries:** {match['team_a']} - {match['team_a_injuries']}, {match['team_b']} - {match['team_b_injuries']}")
        st.write(f"**Odds:** {match['odds']}")

        # Prepare AI prompt (MUST be defined here!)
        prompt = f"""
        Given the following match data:
        - Team A recent form: {match['team_a_form']}
        - Team B recent form: {match['team_b_form']}
        - Team A key injuries: {match['team_a_injuries']}
        - Team B key injuries: {match['team_b_injuries']}
        - Betting odds: {match['odds']}

        Generate a short paragraph predicting the match outcome and explain why.
        """

        # Call AI provider (now prompt is defined!)
        ai_comment = gpt_provider.get_ai_prediction(prompt)
        st.subheader("🤖 AI Prediction")
        st.write(ai_comment)