import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(
    page_title="Grocery Assistant",
    page_icon="🛒",
    layout="wide"
)

DATA_FILE = Path(__file__).with_name("grocery_list.json")

def load_items():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            st.warning("Could not load the saved list. Starting a new list.")
    return []

def save_items(items):
    DATA_FILE.write_text(
        json.dumps(items, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

if "grocery_items" not in st.session_state:
    st.session_state.grocery_items = load_items()

st.title("🛒 Grocery Assistant")
st.write("Plan your shopping, estimate costs, and track purchased items.")

with st.form("add_item", clear_on_submit=True):
    st.subheader("Add a grocery item")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Item name", placeholder="e.g. Milk")
        category = st.selectbox(
            "Category",
            ["Dairy", "Fruits", "Vegetables", "Grains",
             "Snacks", "Household", "Personal Care", "Other"]
        )

    with col2:
        quantity = st.number_input(
            "Quantity", min_value=1, value=1, step=1
        )
        unit = st.selectbox(
            "Unit", ["piece", "kg", "g", "litre", "ml", "pack", "dozen"]
        )

    with col3:
        price = st.number_input(
            "Estimated price per unit (₹)",
            min_value=0.0,
            value=0.0,
            step=5.0
        )
        add = st.form_submit_button("Add to List")

    if add:
        if not name.strip():
            st.warning("Please enter an item name.")
        else:
            st.session_state.grocery_items.append({
                "Item": name.strip(),
                "Category": category,
                "Quantity": int(quantity),
                "Unit": unit,
                "Unit Price (₹)": float(price),
                "Purchased": False
            })
            save_items(st.session_state.grocery_items)
            st.success(f"Added {name.strip()} to your list.")

items = st.session_state.grocery_items

st.divider()
st.subheader("Your Shopping List")

if not items:
    st.info("Your list is empty. Add your first grocery item above.")
else:
    df = pd.DataFrame(items)
    df["Estimated Total (₹)"] = (
        df["Quantity"] * df["Unit Price (₹)"]
    )

    total = df["Estimated Total (₹)"].sum()
    purchased_total = df.loc[
        df["Purchased"], "Estimated Total (₹)"
    ].sum()
    remaining_total = total - purchased_total

    c1, c2, c3 = st.columns(3)
    c1.metric("Estimated Basket Cost", f"₹{total:,.2f}")
    c2.metric("Purchased Cost", f"₹{purchased_total:,.2f}")
    c3.metric("Remaining Cost", f"₹{remaining_total:,.2f}")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Mark Items as Purchased")

    for i, item in enumerate(items):
        label = (
            f"{item['Item']} — {item['Quantity']} {item['Unit']}"
        )
        checked = st.checkbox(
            label,
            value=bool(item["Purchased"]),
            key=f"purchased_{i}"
        )
        if checked != bool(item["Purchased"]):
            item["Purchased"] = checked
            save_items(items)
            st.rerun()

    st.subheader("Manage Your List")

    item_options = [
        f"{i + 1}. {item['Item']}" for i, item in enumerate(items)
    ]
    selected = st.selectbox("Choose an item to remove", item_options)

    if st.button("Remove Selected Item"):
        index = item_options.index(selected)
        items.pop(index)
        save_items(items)
        st.rerun()

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Grocery List (CSV)",
        data=csv_data,
        file_name="grocery_list.csv",
        mime="text/csv"
    )

    if st.button("Clear Entire List"):
        st.session_state.grocery_items = []
        save_items([])
        st.rerun()
