import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Joe Berry - Credit Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Credit Risk Portfolio Dashboard")
st.write("Explore your credit risk portfolio data.")

db_path = Path(__file__).parent / "credit_risk_portfolio.db"

if not db_path.exists():
    st.error("Database file not found.")
    st.stop()

try:
    with sqlite3.connect(str(db_path)) as conn:
        tables = pd.read_sql_query(
            """
            SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name
            """,
            conn
        )

        if tables.empty:
            st.warning("No tables were found in the database.")
        else:
            table_name = st.selectbox(
                "Choose a database table",
                tables["name"].tolist()
            )

            # Table names come from SQLite metadata.
            safe_name = '"' + table_name.replace('"', '""') + '"'
            df = pd.read_sql_query(
                f"SELECT * FROM {safe_name}",
                conn
            )

            st.subheader(f"Portfolio Data: {table_name}")
            st.metric("Total Records", len(df))
            st.dataframe(df, use_container_width=True)

            if not df.empty:
                st.download_button(
                    "Download data as CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    file_name=f"{table_name}.csv",
                    mime="text/csv"
                )

except Exception as e:
    st.error(f"Could not read the database: {e}")
