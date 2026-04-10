import streamlit as st
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Data Cleaning App", layout="wide")

# ------------------ TITLE ------------------
st.title("🧹✨ Data Cleaning Application")
st.markdown("Upload your dataset and clean it بسهولة 🚀")

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

        st.success("✅ File uploaded successfully!")

        # Keep original copy
        cleaned_df = df.copy()

        # -------- PREVIEW --------
        st.subheader("🔍 Original Dataset")
        st.dataframe(df.head())

        # -------- MISSING VALUES --------
        st.subheader("🧼 Missing Values")
        missing = df.isnull().sum()
        st.write(missing[missing > 0])

        # -------- DUPLICATES --------
        st.subheader("📌 Duplicate Records")
        duplicates = df.duplicated().sum()
        st.write(f"Number of duplicate rows: {duplicates}")

        # ------------------ ACTION BUTTONS ------------------

        col1, col2, col3 = st.columns(3)

        # c) Remove missing values
        with col1:
            if st.button("🗑️ Drop Missing Values"):
                cleaned_df = cleaned_df.dropna()
                st.success("Missing values removed!")

        # d) Handle missing values
        with col2:
            if st.button("⚙️ Fill Missing Values"):
                for col in cleaned_df.columns:
                    if cleaned_df[col].dtype == "object":
                        cleaned_df[col].fillna("Unknown", inplace=True)
                    else:
                        cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
                st.success("Missing values handled!")

        # e) Remove duplicates
        with col3:
            if st.button("🚫 Remove Duplicates"):
                cleaned_df = cleaned_df.drop_duplicates()
                st.success("Duplicate rows removed!")

        # -------- SHOW CLEANED DATA --------
        st.subheader("✨ Cleaned Dataset Preview")
        st.dataframe(cleaned_df.head())

        # -------- DOWNLOAD CLEANED FILE --------
        st.subheader("📥 Download Cleaned File")

        file_format = st.selectbox("Select file format", ["CSV", "Excel"])

        if file_format == "CSV":
            csv = cleaned_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

        else:
            from io import BytesIO
            buffer = BytesIO()
            cleaned_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)

            st.download_button(
                label="⬇️ Download Excel",
                data=buffer,
                file_name="cleaned_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("👆 Upload a file to start cleaning!")