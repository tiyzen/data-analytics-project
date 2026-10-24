import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Email Improver",
    page_icon="✉️",
    layout="centered"
)

st.title("✉️ AI Email Improver")
st.write("Improve your emails with clear, professional language using Gemini AI.")

email_text = st.text_area(
    "Enter your email",
    height=220,
    placeholder="Hi sir, I cannot attend the meeting today because I have some work..."
)

tone = st.selectbox(
    "Choose email tone",
    ["Professional", "Friendly", "Formal", "Concise"]
)

if st.button("Improve Email"):
    if not email_text.strip():
        st.warning("Please enter an email first.")
    else:
        try:
            client = genai.Client()

            prompt = f"""
You are a professional email editor.

Improve the email below using the requested tone: {tone}.

Requirements:
- Correct grammar and spelling.
- Improve clarity and readability.
- Preserve the original meaning.
- Do not invent details or commitments.
- Return only the improved email.

Original email:
{email_text}
"""

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            st.subheader("Improved Email")
            st.text_area(
                "Your improved email",
                value=response.text or "No text was returned.",
                height=250
            )

        except Exception as e:
            st.error(f"Could not improve the email: {e}")