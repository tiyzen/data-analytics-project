import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Hotel Booking Assistant",
    page_icon="🏨",
    layout="centered"
)

st.title("🏨 AI Hotel Booking Assistant")
st.write(
    "Generate professional hotel booking replies "
    "using Gemini AI."
)

guest_name = st.text_input(
    "Guest name",
    placeholder="e.g. Rahul"
)

hotel_name = st.text_input(
    "Hotel name",
    placeholder="e.g. Grand Palace Hotel"
)

room_type = st.selectbox(
    "Room type",
    ["Standard", "Deluxe", "Suite", "Family Room"]
)

check_in = st.date_input("Check-in date")
check_out = st.date_input("Check-out date")

guests = st.number_input(
    "Number of guests",
    min_value=1,
    max_value=20,
    value=2
)

request_type = st.selectbox(
    "Guest request",
    [
        "New booking inquiry",
        "Booking confirmation message",
        "Room availability inquiry",
        "Cancellation request",
        "Special request"
    ]
)

extra_details = st.text_area(
    "Additional details",
    placeholder="Mention price, preferences, or other details."
)

tone = st.selectbox(
    "Reply tone",
    ["Professional", "Friendly", "Formal", "Concise"]
)

if st.button("Generate Hotel Reply"):
    if not hotel_name.strip():
        st.warning("Please enter the hotel name.")
    elif check_out <= check_in:
        st.warning("Check-out must be after check-in.")
    else:
        try:
            client = genai.Client()

            prompt = f"""
You are an assistant helping hotel staff write guest replies.

Hotel: {hotel_name}
Guest: {guest_name or "Valued Guest"}
Room type: {room_type}
Check-in: {check_in}
Check-out: {check_out}
Number of guests: {guests}
Request type: {request_type}
Additional details: {extra_details or "None"}
Tone: {tone}

Write a clear, helpful hotel response.

Rules:
- Use the requested tone.
- Include relevant booking details.
- Do not invent room availability, prices, policies,
  confirmation numbers, or completed bookings.
- If availability or confirmation is unknown, say it
  needs to be verified by hotel staff.
- Return only the message to the guest.
"""

            with st.spinner("Generating hotel reply..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            reply = response.text or "No response was returned."

            st.subheader("Generated Hotel Reply")
            st.text_area(
                "Your reply",
                value=reply,
                height=250
            )

            st.download_button(
                "Download Reply",
                data=reply,
                file_name="hotel_reply.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Could not generate the reply: {e}")
