import streamlit as st
from transformers import pipeline

st.set_page_config(
    page_title="GPT-2 Text Generator",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ GPT-2 Text Generator")
st.write("Generate text continuations using a pretrained GPT-2 model.")

@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="openai-community/gpt2"
    )

prompt = st.text_area(
    "Enter your starting text",
    height=150,
    placeholder="Once upon a time, in a small village..."
)

max_tokens = st.slider(
    "Maximum new tokens",
    min_value=30,
    max_value=200,
    value=80,
    step=10
)

temperature = st.slider(
    "Creativity",
    min_value=0.2,
    max_value=1.5,
    value=0.8,
    step=0.1
)

if st.button("Generate Text"):
    if not prompt.strip():
        st.warning("Please enter some starting text.")
    else:
        try:
            with st.spinner("Loading GPT-2 and generating text..."):
                model = load_model()
                result = model(
                    prompt,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=temperature,
                    top_k=50,
                    num_return_sequences=1,
                    pad_token_id=50256
                )

            generated_text = result[0]["generated_text"]

            st.subheader("Generated Text")
            st.write(generated_text)

            st.download_button(
                "Download Generated Text",
                data=generated_text,
                file_name="generated_text.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Text generation failed: {e}")
