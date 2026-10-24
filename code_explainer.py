import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Python Code Explainer",
    page_icon="🐍",
    layout="wide"
)

st.title("🐍 AI Python Code Explainer")
st.write("Understand Python code with clear, step-by-step explanations.")

code = st.text_area(
    "Paste your Python code",
    height=300,
    placeholder="def add(a, b):\n    return a + b"
)

level = st.selectbox(
    "Explanation level",
    ["Beginner", "Intermediate", "Advanced"]
)

detail = st.selectbox(
    "Explanation style",
    [
        "Line by line",
        "Overall summary",
        "Find bugs and explain fixes",
        "Explain time and space complexity"
    ]
)

question = st.text_input(
    "Optional question",
    placeholder="e.g. Why is a dictionary used here?"
)

if st.button("Explain Code"):
    if not code.strip():
        st.warning("Please paste some Python code first.")
    else:
        try:
            client = genai.Client()

            prompt = f"""
You are a Python programming tutor.

Explain the following Python code.
Audience level: {level}
Requested explanation: {detail}
Additional question: {question or "None"}

Requirements:
- Be accurate and easy to understand.
- Use headings and examples where useful.
- For line-by-line mode, explain the important lines in order.
- For bug-fixing mode, identify likely bugs and show corrected code.
- For complexity mode, explain time and space complexity only
  where it can be reasonably determined.
- Never claim code was executed or tested unless it actually was.

Python code:
```python
{code}
```
"""

            with st.spinner("Analysing your code..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            explanation = response.text or "No explanation was returned."

            st.subheader("Explanation")
            st.markdown(explanation)

            st.download_button(
                "Download Explanation",
                data=explanation,
                file_name="python_code_explanation.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Could not explain the code: {e}")
