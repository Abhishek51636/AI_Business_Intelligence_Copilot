import streamlit as st
from io import BytesIO
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def reports_module(df):

    st.subheader("📄 Analysis Report")

    dataset_name = st.text_input(
        "Dataset Name",
        "Business Dataset"
    )

    if st.button("Generate PDF Report"):

        filename = "AI_Business_Report.pdf"

        c = canvas.Canvas(
            filename,
            pagesize=letter
        )

        width, height = letter

        y = height - 50

        # -------------------------
        # TITLE
        # -------------------------

        c.setFont(
            "Helvetica-Bold",
            18
        )

        c.drawString(
            50,
            y,
            "AI Business Intelligence Copilot"
        )

        y -= 30

        c.setFont(
            "Helvetica",
            12
        )

        c.drawString(
            50,
            y,
            "Dataset Analysis Report"
        )

        y -= 40

        # -------------------------
        # DATASET OVERVIEW
        # -------------------------

        c.setFont(
            "Helvetica-Bold",
            14
        )

        c.drawString(
            50,
            y,
            "1. Dataset Overview"
        )

        y -= 25

        c.setFont(
            "Helvetica",
            11
        )

        c.drawString(
            60,
            y,
            f"Dataset Name: {dataset_name}"
        )

        y -= 20

        c.drawString(
            60,
            y,
            f"Rows: {df.shape[0]}"
        )

        y -= 20

        c.drawString(
            60,
            y,
            f"Columns: {df.shape[1]}"
        )

        y -= 30

        # -------------------------
        # FEATURES
        # -------------------------

        c.setFont(
            "Helvetica-Bold",
            14
        )

        c.drawString(
            50,
            y,
            "2. Dataset Features"
        )

        y -= 25

        c.setFont(
            "Helvetica",
            11
        )

        for col in df.columns:
            if y < 80:
                c.showPage()
                y = 750
            c.drawString(
                70,
                y,
                f"• {col}"
            )

            y -= 18

            if y < 100:

                c.showPage()

                y = height - 50

        # -------------------------
        # DATA QUALITY
        # -------------------------

        missing = int(
            df.isnull()
            .sum()
            .sum()
        )

        duplicates = int(
            df.duplicated()
            .sum()
        )

        numeric_cols = len(
            df.select_dtypes(
                include=["number"]
            ).columns
        )

        categorical_cols = len(
            df.select_dtypes(
                exclude=["number"]
            ).columns
        )

        c.setFont(
            "Helvetica-Bold",
            14
        )

        c.drawString(
            50,
            y,
            "3. Data Quality Analysis"
        )
        if y < 80:
            c.showPage()
            y = 750
        y -= 25

        c.setFont(
            "Helvetica",
            11
        )

        c.drawString(
            60,
            y,
            f"Missing Values: {missing}"
        )
        if y < 80:
            c.showPage()
            y = 750
        y -= 20

        c.drawString(
            60,
            y,
            f"Duplicate Rows: {duplicates}"
        )

        y -= 20

        c.drawString(
            60,
            y,
            f"Numeric Columns: {numeric_cols}"
        )

        y -= 20

        c.drawString(
            60,
            y,
            f"Categorical Columns: {categorical_cols}"
        )

        y -= 30

        # -------------------------
        # MACHINE LEARNING
        # -------------------------

        c.setFont(
            "Helvetica-Bold",
            14
        )
        
        c.drawString(
            50,
            y,
            "4. Machine Learning Summary"
        )

        y -= 25
        if y < 80:
            c.showPage()
            y = 750
        c.setFont(
            "Helvetica",
            11
        )

        c.drawString(
            60,
            y,
            "Model Used: User Selected Model"
        )

        y -= 20
        if y < 80:
            c.showPage()
            y = 750
        c.drawString(
            60,
            y,
            "Prediction Module Executed"
        )

        y -= 30

        # -------------------------
        # INSIGHTS
        # -------------------------

        c.setFont(
            "Helvetica-Bold",
            14
        )

        c.drawString(
            50,
            y,
            "5. Key Insights"
        )

        y -= 25

        c.setFont(
            "Helvetica",
            11
        )

        c.drawString(
            60,
            y,
            f"Dataset contains {df.shape[0]} records."
        )

        y -= 20
        if y < 80:
            c.showPage()
            y = 750
        c.drawString(
            60,
            y,
            f"Total missing values: {missing}"
        )

        y -= 20
        if y < 80:
            c.showPage()
            y = 750
        c.drawString(
            60,
            y,
            f"Total duplicate rows: {duplicates}"
        )

        y -= 20

        if numeric_cols > 0:

            highest_avg = (

                df.select_dtypes(
                    include=["number"]
                )

                .mean()

                .idxmax()

            )

            c.drawString(
                60,
                y,
                f"{highest_avg} has highest average value."
            )

            y -= 20
            if y < 80:
                c.showPage()
                y = 750
        # -------------------------
        # EXECUTIVE SUMMARY
        # -------------------------

        y -= 10

        c.setFont(
            "Helvetica-Bold",
            14
        )

        c.drawString(
            50,
            y,
            "6. Executive Summary"
        )

        y -= 25

        c.setFont(
            "Helvetica",
            11
        )

        summary = [
            "Dataset successfully analyzed.",
            "Data quality metrics calculated.",
            "Business insights generated.",
            "Visualization and ML modules executed.",
            "Report generated using AI Business Intelligence Copilot."
        ]

        for line in summary:

            c.drawString(
                60,
                y,
                line
            )

            y -= 20
            if y < 80:
                c.showPage()
                y = 750
        c.save()

        st.success(
            "PDF Report Generated Successfully"
        )

        with open(
            filename,
            "rb"
        ) as pdf_file:

            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_file,
                file_name=filename,
                mime="application/pdf"
            )


    st.subheader(
        "📄 Reports & Downloads"
    )

    excel_file = BytesIO()

    with pd.ExcelWriter(
        excel_file,
        engine="openpyxl"
    ) as writer:

        df.to_excel(

            writer,

            index=False,

            sheet_name="Cleaned_Data"

        )

    st.download_button(

        label="⬇ Download Cleaned Excel",

        data=excel_file.getvalue(),

        file_name="cleaned_dataset.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )