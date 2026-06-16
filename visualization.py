import streamlit as st
import plotly.express as px

def visualization_module(df):

    st.subheader(
        "📈 Visualization Module"
    )

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    if len(numeric_cols) == 0:

        st.warning(
            "No numeric columns available"
        )

        return

    chart_type = st.selectbox(

        "Select Chart",

        [

            "Histogram",

            "Scatter Plot",

            "Bar Chart",

            "Box Plot",

            "Line Chart"

        ]

    )

    if chart_type == "Histogram":

        column = st.selectbox(

            "Choose Column",

            numeric_cols

        )

        fig = px.histogram(

            df,

            x=column

        )

    elif chart_type == "Scatter Plot":

        x_axis = st.selectbox(

            "X Axis",

            numeric_cols

        )

        y_axis = st.selectbox(

            "Y Axis",

            numeric_cols,

            index=1 if len(numeric_cols) > 1 else 0

        )

        fig = px.scatter(

            df,

            x=x_axis,

            y=y_axis

        )

    elif chart_type == "Bar Chart":

        x_col = st.selectbox(

            "X Column",

            df.columns

        )

        y_col = st.selectbox(

            "Y Column",

            numeric_cols

        )

        fig = px.bar(

            df,

            x=x_col,

            y=y_col

        )

    elif chart_type == "Box Plot":

        col = st.selectbox(

            "Column",

            numeric_cols

        )

        fig = px.box(

            df,

            y=col

        )

    else:

        x_col = st.selectbox(

            "X Axis",

            df.columns

        )

        y_col = st.selectbox(

            "Y Axis",

            numeric_cols

        )

        fig = px.line(

            df,

            x=x_col,

            y=y_col

        )

    st.plotly_chart(

        fig,

        use_container_width=True

    )