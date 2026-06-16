import streamlit as st
import pandas as pd

def insights_module(df):
    st.subheader(
        "🧠 Dataset Insights"
    )

    # -------------------------
    # BASIC METRICS
    # -------------------------

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Rows",
        df.shape[0]
    )
    c2.metric(
        "Columns",
        df.shape[1]
    )
    c3.metric(
        "Missing",
        int(df.isnull().sum().sum())
    )
    c4.metric(
        "Duplicates",
        int(df.duplicated().sum())
    )

    # -------------------------
    # COLUMN INFO
    # -------------------------

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Datatype": df.dtypes.astype(str),
        "Missing": df.isnull().sum(),
        "Unique": df.nunique()
    })
    st.dataframe(
        info_df,
        use_container_width=True
    )
    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    # -------------------------
    # KPI CARDS
    # -------------------------

    st.subheader(
        "📊 Business KPI"
    )
    if len(numeric_cols) > 0:
        metric_col = st.selectbox(
            "Choose KPI Column",
            numeric_cols
        )
        k1, k2, k3, k4 = st.columns(4)
        k1.metric(
            "Total",
            round(
                df[metric_col].sum(),
                2
            )
        )

        k2.metric(
            "Average",
            round(
                df[metric_col].mean(),
                2
            )
        )

        k3.metric(
            "Highest",
            round(
                df[metric_col].max(),
                2
            )
        )

        k4.metric(
            "Lowest",
            round(
                df[metric_col].min(),
                2
            )
        )

    # -------------------------
    # STATISTICS
    # -------------------------

    if len(numeric_cols) > 0:
        st.subheader(
            "Statistics"
        )
        st.dataframe(
            df[numeric_cols]
            .describe()
            .T,
            use_container_width=True
        )
        for col in numeric_cols:
            st.info(
                f"{col} | Mean={round(df[col].mean(),2)} | Median={round(df[col].median(),2)}"
            )

    # -------------------------
    # MISSING %
    # -------------------------

    st.subheader(
        "Missing Value Percentage"
    )
    missing_table = (
        df.isnull().sum()
        / len(df)
    ) * 100
    profile_df = pd.DataFrame({
        "Column": df.columns,
        "Missing %": missing_table.round(2)
    })
    st.dataframe(
        profile_df,
        use_container_width=True
    )

    # -------------------------
    # DATASET PROFILING
    # -------------------------

    st.subheader(
        "📊 Dataset Profiling"
    )
    categorical_cols = df.select_dtypes(
        exclude=["number"]
    ).columns.tolist()
    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Numeric Columns",
        len(numeric_cols)
    )
    c2.metric(
        "Categorical Columns",
        len(categorical_cols)
    )
    c3.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )

    # -------------------------
    # UNIQUE VALUES
    # -------------------------

    st.subheader(
        "Unique Value Analysis"
    )
    unique_df = pd.DataFrame({
        "Column": df.columns,
        "Unique Values": df.nunique()
    })
    st.dataframe(
        unique_df,
        use_container_width=True
    )

    # -------------------------
    # DISTRIBUTION ANALYSIS
    # -------------------------

    if len(numeric_cols) > 0:
        st.subheader(
            "Distribution Analysis"
        )
        skew_df = pd.DataFrame({
            "Column": numeric_cols,
            "Skewness": [
                round(
                    df[col].skew(),
                    2
                )
                for col in numeric_cols
            ]
        })
        st.dataframe(
            skew_df,
            use_container_width=True
        )
    missing = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())
    score = 100
    score -= min(missing, 30)
    score -= min(duplicates * 2, 20)
    score = max(score, 0)
    if score >= 90:
        status = "🟢 Excellent Dataset"
    elif score >= 70:
        status = "🟡 Needs Cleaning"
    else:
        status = "🔴 Poor Quality Dataset"
    st.subheader("🏥 Dataset Health Score")
    c1, c2 = st.columns(2)
    c1.metric(
    "Quality Score",
    f"{score}/100"
)
    c2.metric(
    "Status",
    status
)
    st.progress(score / 100)

# =========================
# EXECUTIVE SUMMARY
# =========================

    st.subheader(
    "📋 Executive Summary"
)
    rows = df.shape[0]
    cols = df.shape[1]
    missing = int(
        df.isnull().sum().sum()
)
    duplicates = int(
        df.duplicated().sum()
)
    missing_percent = round(
        (missing / (rows * cols)) * 100,2
)
    numeric_cols = df.select_dtypes(
        include=["number"]
).columns
    correlation_text = "No numeric correlation found"
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        corr_pairs = (
            corr_matrix.unstack()
            .sort_values(
            ascending=False
        )
    )
        corr_pairs = corr_pairs[
        corr_pairs < 1
    ]
    if len(corr_pairs) > 0:
        top_corr = corr_pairs.index[0]
        correlation_text = (
            f"{top_corr[0]} and "
            f"{top_corr[1]}"
        )
    st.markdown(
f"""
<div style="
padding:20px;
border-radius:18px;
background:rgba(255,255,255,0.08);
backdrop-filter:blur(15px);
border:1px solid rgba(255,255,255,0.08);
">



<p>
Dataset contains <b>{rows}</b> rows and
<b>{cols}</b> columns.
</p>

<p>
Missing values account for
<b>{missing_percent}%</b> of the dataset.
</p>

<p>
Duplicate records found:
<b>{duplicates}</b>
</p>

<p>
Strongest correlation detected between:
<b>{correlation_text}</b>
</p>

<p>
Dataset appears suitable for
exploratory analysis and
machine learning workflows.
</p>
</div>
""",
unsafe_allow_html=True
)