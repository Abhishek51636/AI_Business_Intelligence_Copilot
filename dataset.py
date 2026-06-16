import streamlit as st
import pandas as pd
def dataset_module(df):
    st.subheader(
        "Dataset Preview"
    )
    st.dataframe(
        df.head(20),
        use_container_width=True
    )

# -------------------------
# COLUMN NAMES
# -------------------------

    st.subheader(
    "📋 Dataset Columns"
)
    col_df = pd.DataFrame({
    "Column Names": df.columns
})
    st.dataframe(
    col_df,
    use_container_width=True
)
    st.info(
    f"Total Columns: {len(df.columns)}"
)