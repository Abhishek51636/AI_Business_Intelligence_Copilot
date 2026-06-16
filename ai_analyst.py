import streamlit as st
from openai import OpenAI

# -----------------------------
# OPENROUTER CLIENT
# -----------------------------

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# -----------------------------
# AI ANALYST MODULE
# -----------------------------

def ai_analyst_module(df):

    st.subheader(
        "🤖 AI Dataset Analyst"
    )

    # -----------------------------
    # DATASET ANALYSIS
    # -----------------------------

    if st.button(
        "Generate AI Insights"
    ):

        with st.spinner(
            "Analyzing Dataset..."
        ):

            sample = df.head(20).to_string()

            prompt = f"""
Analyze this dataset.

Dataset Shape:
{df.shape}

Columns:
{list(df.columns)}

Sample Data:
{sample}

Provide:

1. Dataset Overview
2. Data Quality Analysis
3. Business Insights
4. Recommendations
5. Suitable Machine Learning Models
"""

            try:

                response = client.chat.completions.create(

                    model="deepseek/deepseek-chat-v3",

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]

                )

                st.success(
                    "Analysis Completed"
                )

                st.write(
                    response.choices[0]
                    .message
                    .content
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

    st.markdown("---")

    # -----------------------------
    # CHAT WITH DATASET
    # -----------------------------

    st.subheader(
        "💬 Chat With Dataset"
    )

    question = st.text_input(
        "Ask a question about your dataset"
    )

    if st.button(
        "Ask AI"
    ):

        if question:

            with st.spinner(
                "Thinking..."
            ):

                sample = df.head(10).to_string()

                prompt = f"""
Dataset Columns:
{list(df.columns)}

Sample Data:
{sample}

Question:
{question}

Answer only based on the dataset.
"""

                try:

                    response = client.chat.completions.create(

                        model="deepseek/deepseek-chat-v3",

                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]

                    )

                    st.success(
                        response.choices[0]
                        .message
                        .content
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )