import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI WhatsApp Reply Generator",
    page_icon="💬",
    layout="centered"
)

st.title("💬 AI WhatsApp Reply Generator")
st.write("Generate natural WhatsApp replies in seconds.")

message = st.text_area(
    "Incoming WhatsApp message",
    height=150,
    placeholder="Paste the message you received here..."
)

tone = st.selectbox(
    "Choose reply tone",
    [
        "Friendly",
        "Professional",
        "Funny",
        "Polite",
        "Casual",
        "Romantic",
        "Apologetic"
    ]
)

language = st.selectbox(
    "Reply language",
    ["English", "Hindi", "Hinglish"]
)

length = st.selectbox(
    "Reply length",
    ["Short", "Medium", "Detailed"]
)

context = st.text_input(
    "Optional context",
    placeholder="e.g. Replying to a friend who invited me to dinner"
)

if st.button("Generate Reply"):
    if not message.strip():
        st.warning("Please paste a WhatsApp message first.")
    else:
        try:
            client = genai.Client()

            prompt = f"""
You are an expert WhatsApp reply-writing assistant.

Incoming message:
{message}

Requested tone: {tone}
Language: {language}
Length: {length}
Context: {context or "No extra context provided"}

Instructions:
- Write a natural reply suitable for WhatsApp.
- Match the requested tone and language.
- Keep the reply within the requested length.
- Do not invent personal facts or commitments.
- Do not answer as if you know details that were not provided.
- Return only the suggested reply.
"""

            with st.spinner("Generating your reply..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            reply = response.text or "No reply was returned."

            st.subheader("Your Suggested Reply")
            st.text_area(
                "Generated message",
                value=reply,
                height=180
            )

            st.button(
                "Copy-ready reply",
                on_click=None,
                disabled=True
            )

            st.download_button(
                "Download Reply",
                data=reply,
                file_name="whatsapp_reply.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Could not generate the reply: {e}")
