import streamlit as st
from transformers import pipeline

st.set_page_config(
    page_title="AI Question Answer Generator",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Question Answer Generator")
st.write("Ask questions about a passage using a local AI model.")

@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small"
    )

context = st.text_area(
    "Enter the passage or information",
    height=220,
    placeholder="Paste the text you want to ask questions about..."
)

question = st.text_input(
    "Your question",
    placeholder="e.g. What is the main idea?"
)

if st.button("Generate Answer"):
    if not context.strip() or not question.strip():
        st.warning("Please enter both a passage and a question.")
    else:
        try:
            with st.spinner(
                "Loading the local AI model and generating an answer..."
            ):
                model = load_model()
                prompt = (
                    "Answer the question using only the context. "
                    "If the answer is not in the context, say "
                    "'The passage does not provide this information.' "
                    f"Context: {context[:3000]} "
                    f"Question: {question} "
                    "Answer:"
                )
                result = model(
                    prompt,
                    max_new_tokens=120,
                    do_sample=False
                )

            answer = result[0]["generated_text"].strip()

            st.subheader("Answer")
            st.write(answer)

            st.download_button(
                "Download Answer",
                data=answer,
                file_name="answer.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Could not generate an answer: {e}")
