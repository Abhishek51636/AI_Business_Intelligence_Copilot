import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_squared_error


def ml_module(df):

    st.subheader(
        "🤖 Machine Learning"
    )

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    if len(numeric_cols) < 2:

        st.warning(
            "Need minimum 2 numeric columns"
        )

        return

    target = st.selectbox(

        "Target Column",

        numeric_cols

    )

    features = [

        col for col in numeric_cols

        if col != target

    ]

    ml_df = df[
        features + [target]
    ].dropna()

    if len(ml_df) < 5:

        st.warning(
            "Not enough data"
        )

        return

    X = ml_df[features]

    y = ml_df[target]

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42

    )

    # -------------------------
    # MODEL SELECTION
    # -------------------------

    model_choice = st.selectbox(

        "Choose Model",

        [

            "Linear Regression",

            "Random Forest",

            "Decision Tree"

        ]

    )

    if model_choice == "Linear Regression":

        model = LinearRegression()

    elif model_choice == "Random Forest":

        model = RandomForestRegressor(

            n_estimators=100,

            random_state=42

        )

    else:

        model = DecisionTreeRegressor(

            random_state=42

        )

    # -------------------------
    # TRAIN MODEL
    # -------------------------

    with st.spinner(

        f"Training {model_choice}..."

    ):

        model.fit(

            X_train,

            y_train

        )

        pred = model.predict(
            X_test
        )

    score = r2_score(

        y_test,

        pred

    )

    mse = mean_squared_error(

        y_test,

        pred

    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "R² Score",

            round(score,3)

        )

    with c2:

        st.metric(

            "MSE",

            round(mse,3)

        )

    st.success(

        f"{model_choice} Completed"

    )

    result = X_test.copy()

    result["Actual"] = y_test.values

    result["Predicted"] = pred

    st.dataframe(

        result.head(),

        use_container_width=True

    )

    st.subheader(
        "Model Information"
    )

    st.write(

        f"Selected Model: {model_choice}"

    )

    st.write(

        f"Features Used: {len(features)}"

    )

    st.write(

        f"Training Samples: {len(X_train)}"

    )

    # -------------------------
    # AUTO MODEL RECOMMENDATION
    # -------------------------

    st.subheader(
        "🏆 Auto Model Recommendation"
    )

    models = {

        "Linear Regression": LinearRegression(),

        "Random Forest": RandomForestRegressor(

            n_estimators=100,

            random_state=42

        ),

        "Decision Tree": DecisionTreeRegressor(

            random_state=42

        )

    }

    scores = {}

    with st.spinner(

        "Comparing models..."

    ):

        for name, temp_model in models.items():

            temp_model.fit(

                X_train,

                y_train

            )

            temp_pred = temp_model.predict(

                X_test

            )

            temp_score = r2_score(

                y_test,

                temp_pred

            )

            scores[name] = round(

                temp_score,

                3

            )

    compare_df = pd.DataFrame({

        "Model": list(scores.keys()),

        "R² Score": list(scores.values())

    })

    st.dataframe(

        compare_df,

        use_container_width=True

    )

    best_model = max(

        scores,

        key=scores.get

    )

    st.success(

        f"Recommended Model: {best_model}"

    )

    st.metric(

        "Best Model Score",

        scores[best_model]

    )

    # -------------------------
    # HEATMAP
    # -------------------------

    st.subheader(
        "🔥 Correlation Heatmap"
    )

    corr = df[
        numeric_cols
    ].corr()

    fig, ax = plt.subplots(
        figsize=(8,6)
    )

    heat = ax.imshow(
        corr,
        aspect="auto"
    )

    plt.colorbar(
        heat
    )

    ax.set_xticks(
        range(len(corr.columns))
    )

    ax.set_xticklabels(
        corr.columns,
        rotation=90
    )

    ax.set_yticks(
        range(len(corr.columns))
    )

    ax.set_yticklabels(
        corr.columns
    )

    st.pyplot(
        fig
    )