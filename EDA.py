import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="EDA App", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    h1 {
        color: #4A90E2;
        text-align: center;
    }
    h2, h3 {
        color: #34495E;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📊✨ Interactive EDA Dashboard")
st.markdown("Upload your dataset and explore insights visually 🚀")

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader(
    "📂 Upload CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    file_name = uploaded_file.name

    try:
        # -------- READ FILE --------
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("❌ Unsupported file type")
            st.stop()

        # ✅ FIX: Convert churn column to text (avoid checkbox UI)
        if "churn" in df.columns:
            df["churn"] = df["churn"].astype(str)

        st.success("✅ File uploaded successfully!")

        
        # -------- PREVIEW --------
        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head())

        # -------- INFO --------
        st.subheader("📌 Dataset Info")
        col1, col2 = st.columns(2)
        col1.metric("Rows 📏", df.shape[0])
        col2.metric("Columns 📐", df.shape[1])

        # -------- DATA TYPES --------
        numerical_cols = df.select_dtypes(include=["number"])
        categorical_cols = df.select_dtypes(exclude=["number"])

        # -------- NUMERICAL SUMMARY --------
        st.subheader("📈 Numerical Features Summary")
        if not numerical_cols.empty:
            st.write(numerical_cols.describe())

            # Histogram
            st.subheader("📊 Distribution Plots")
            selected_num_col = st.selectbox(
                "Select a numerical column",
                numerical_cols.columns
            )

            fig, ax = plt.subplots()
            sns.histplot(df[selected_num_col], kde=True, color="#4A90E2", ax=ax)
            st.pyplot(fig)

        else:
            st.info("⚠️ No numerical features found.")

        # -------- CATEGORICAL SUMMARY --------
        if not categorical_cols.empty:
            st.subheader("📊 Categorical Features Summary")
            st.write(categorical_cols.describe())

            # Bar chart
            st.subheader("📊 Categorical Distribution")
            selected_cat_col = st.selectbox(
                "Select a categorical column",
                categorical_cols.columns
            )

            fig, ax = plt.subplots(figsize=(12,6))
            df[selected_cat_col].value_counts().plot(
                kind="bar",
                color="#50C878",
                ax=ax
            )
            st.pyplot(fig)

        else:
            st.info("⚠️ No non-numerical (categorical) features found.")

        # -------- CORRELATION --------
        if not numerical_cols.empty:
            st.subheader("🔥 Correlation Heatmap")

            fig, ax = plt.subplots(figsize=(15, 10))
            sns.heatmap(
                numerical_cols.corr(),
                annot=True,
                cmap="coolwarm",
                ax=ax
            )
            st.pyplot(fig)

        # -------- MISSING VALUES --------
        st.subheader("🧼 Missing Values Overview")
        missing = df.isnull().sum()

        if missing.sum() > 0:
            st.write(missing[missing > 0])

            fig, ax = plt.subplots()
            missing[missing > 0].plot(
                kind="bar",
                color="#FF6F61",
                ax=ax
            )
            st.pyplot(fig)
        else:
            st.success("🎉 No missing values found!")

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")

else:
    st.info("👆 Upload a file to start your EDA journey!")