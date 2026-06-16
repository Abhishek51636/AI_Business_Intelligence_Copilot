import streamlit as st
import pandas as pd

def cleaning_module(df):
    st.subheader("🧹 Data Cleaning")

    # Initialize cleaned dataframe
    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = df.copy()
    working_df = st.session_state.cleaned_df.copy()

    # -------------------------
    # Missing Values Summary
    # -------------------------

    st.subheader("Missing Values")
    missing_df = pd.DataFrame({
        "Column": working_df.columns,
        "Missing Values": working_df.isnull().sum()
    })

    st.dataframe(
        missing_df,
        use_container_width=True
    )

    # -------------------------
    # Handle Missing Values
    # -------------------------

    if st.button(
        "Replace Missing Values"
    ):
        numeric_cols = working_df.select_dtypes(
            include=["number"]
        ).columns
        categorical_cols = working_df.select_dtypes(
            exclude=["number"]
        ).columns
        working_df[numeric_cols] = working_df[
            numeric_cols
        ].fillna(0)
        working_df[categorical_cols] = working_df[
            categorical_cols
        ].fillna("None")

        st.session_state.cleaned_df = working_df
        st.success(
            "Missing values handled successfully"
        )

    # -------------------------
    # Duplicate Removal
    # -------------------------

    st.subheader(
        "Remove Duplicates"
    )
    duplicate_column = st.selectbox(
        "Select Column",
        working_df.columns
    )
    if st.button(
        "Remove Duplicates"
    ):
        before_rows = len(
            working_df
        )
        working_df = working_df.drop_duplicates(
            subset=[duplicate_column]
        )
        removed_rows = before_rows - len(
            working_df
        )

        st.session_state.cleaned_df = working_df
        st.success(
            f"{removed_rows} duplicate rows removed based on '{duplicate_column}'"
        )

    # -------------------------
    # Dataset Statistics
    # -------------------------

    st.subheader(
        "Cleaning Summary"
    )
    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Rows",
        st.session_state.cleaned_df.shape[0]
    )
    c2.metric(
        "Columns",
        st.session_state.cleaned_df.shape[1]
    )
    c3.metric(
        "Missing Values",
        int(
            st.session_state.cleaned_df
            .isnull()
            .sum()
            .sum()
        )
    )

    # -------------------------
    # Preview
    # -------------------------

    st.subheader(
        "Cleaned Dataset Preview"
    )
    st.dataframe(
        st.session_state.cleaned_df.head(20),
        use_container_width=True
    )
    return st.session_state.cleaned_df