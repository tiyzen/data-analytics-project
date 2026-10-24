import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="Expense Helper",
    page_icon="💰",
    layout="wide"
)

DATA_FILE = Path(__file__).with_name("expenses.json")

def load_expenses():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return pd.DataFrame(data)
        except (json.JSONDecodeError, OSError):
            st.warning("Could not read saved expenses. Starting with an empty list.")
    return pd.DataFrame(
        columns=["Date", "Description", "Category", "Type", "Amount"]
    )

def save_expenses(df):
    DATA_FILE.write_text(
        df.to_json(orient="records", date_format="iso", indent=2),
        encoding="utf-8"
    )

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

st.title("💰 Expense Helper")
st.write("Record expenses and income, review your spending, and export your records.")

with st.form("expense_form", clear_on_submit=True):
    st.subheader("Add a transaction")

    col1, col2 = st.columns(2)

    with col1:
        transaction_date = st.date_input("Date", value=date.today())
        description = st.text_input("Description", placeholder="e.g. Groceries")
        category = st.selectbox(
            "Category",
            ["Food", "Transport", "Shopping", "Bills",
             "Education", "Health", "Entertainment", "Salary", "Other"]
        )

    with col2:
        transaction_type = st.selectbox("Transaction type", ["Expense", "Income"])
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        submitted = st.form_submit_button("Save Transaction")

    if submitted:
        if not description.strip():
            st.warning("Enter a transaction description.")
        elif amount <= 0:
            st.warning("Amount must be greater than zero.")
        else:
            new_row = {
                "Date": transaction_date.isoformat(),
                "Description": description.strip(),
                "Category": category,
                "Type": transaction_type,
                "Amount": float(amount)
            }

            updated = pd.concat(
                [st.session_state.expenses, pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.session_state.expenses = updated
            save_expenses(updated)
            st.success("Transaction saved.")

df = st.session_state.expenses.copy()

st.divider()
st.subheader("Your Summary")

if df.empty:
    st.info("No transactions yet. Add one above to begin.")
else:
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    income = df.loc[df["Type"] == "Income", "Amount"].sum()
    expenses = df.loc[df["Type"] == "Expense", "Amount"].sum()
    balance = income - expenses

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Income", f"₹{income:,.2f}")
    c2.metric("Total Expenses", f"₹{expenses:,.2f}")
    c3.metric("Net Balance", f"₹{balance:,.2f}")

    st.subheader("Transactions")
    st.dataframe(df, use_container_width=True, hide_index=True)

    expense_rows = df[df["Type"] == "Expense"]
    if not expense_rows.empty:
        st.subheader("Expenses by Category")
        category_totals = expense_rows.groupby("Category")["Amount"].sum()
        st.bar_chart(category_totals)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Transactions CSV",
        data=csv_data,
        file_name="expense_transactions.csv",
        mime="text/csv"
    )

    st.subheader("Delete a Transaction")
    row_number = st.number_input(
        "Transaction row number (starting at 1)",
        min_value=1,
        max_value=len(df),
        step=1
    )

    if st.button("Delete Selected Row"):
        updated = df.drop(df.index[int(row_number) - 1]).reset_index(drop=True)
        st.session_state.expenses = updated
        save_expenses(updated)
        st.rerun()
