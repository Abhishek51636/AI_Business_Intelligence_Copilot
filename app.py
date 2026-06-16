import streamlit as st
import pandas as pd
from dataset import dataset_module
from cleaning import cleaning_module
from visualization import visualization_module
from ml import ml_module
from insights import insights_module
from reports import reports_module
from ai_analyst import ai_analyst_module

st.set_page_config(
    page_title="AI Business Intelligence Copilot",
    page_icon="📊",
    layout="wide"
)

# ---------------- CSS ----------------

def load_css():
    with open(
        "style.css"
    ) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
load_css()

# ---------------- HERO ---------------

st.markdown(
"""
<div class='hero'>
<h1>
AI Business Intelligence Copilot
</h1>
<p>
Upload → Analyze → Visualize → Predict
</p>
</div>
""",
unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------

st.sidebar.markdown(
"""
# 🚀 Navigation
### AI Modules
"""
)

module = st.sidebar.radio(
   "Choose Module",
    [

        "Dataset",

        "Cleaning",

        "Visualization",

        "Machine Learning",

        "Insights",

        "AI Analyst",

        "Reports"

    ]
)
st.write("Current Module:", module)
st.sidebar.markdown(
"""
<div style="
padding:10px;
border-radius:12px;
text-align:center;
background:linear-gradient(
90deg,
#3b82f6,
#8b5cf6
);
font-weight:bold;
color:white;
margin-bottom:15px;
">
🤖 Powered by Ollama
</div>
""",
unsafe_allow_html=True
)
# ---------------- Upload ----------------

uploaded_file = st.file_uploader(
    "Upload CSV / Excel",
    type=["csv","xlsx"]
)

if uploaded_file is None:
    st.info(
        "Upload dataset first"
    )
    st.stop()

# ---------------- Dataset Read ----------------

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Store original dataset once
    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = df.copy()
# ---------------- KPI Cards ----------------

missing = int(
    df.isnull().sum().sum()
)
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown(
    f"""
    <div class='metric-card'>
    <h2>{df.shape[0]}</h2>
    <p>Rows</p>
    </div>
    """,
    unsafe_allow_html=True
    )

with c2:
    st.markdown(
    f"""
    <div class='metric-card'>
    <h2>{df.shape[1]}</h2>
    <p>Columns</p>
    </div>
    """,
    unsafe_allow_html=True
    )

with c3:
    st.markdown(
    f"""
    <div class='metric-card'>
    <h2>{missing}</h2>
    <p>Missing</p>
    </div>
    """,
    unsafe_allow_html=True
    )
st.markdown("---")

# ---------------- Navigation ----------------

if module == "Dataset":
    dataset_module(st.session_state.cleaned_df)
elif module == "Cleaning":
    cleaning_module(st.session_state.cleaned_df)
elif module == "Visualization":
    visualization_module(st.session_state.cleaned_df)
elif module == "Machine Learning":
    ml_module(st.session_state.cleaned_df)
elif module == "Insights":
    insights_module(st.session_state.cleaned_df)
elif module == "AI Analyst":
    ai_analyst_module(st.session_state.cleaned_df)
elif module == "Reports":
    reports_module(st.session_state.cleaned_df)

st.markdown("---")
st.markdown(
"""
<div style="
text-align:center;
padding:15px;
color:#9ca3af;
">
Version 1.0
<br>
Created by Abhishek 🤖
</div>
""",
unsafe_allow_html=True
)
