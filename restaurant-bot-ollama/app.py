# app.py
import streamlit as st
import json

st.set_page_config(page_title="Restaurant Bot", page_icon="🍕")
st.title("🍕 Pizza Restaurant Bot")
st.write("Welcome! Ask me anything about our menu or place an order.")

# Load menu from JSON file
with open("menu.json", "r") as f:
    menu = json.load(f)

st.subheader("Menu")
for m in menu:
    st.write(f"{m['item']} - ${m['price']}")

# User input
user_input = st.text_input("Ask the bot:")

if user_input:
    # Mock response instead of calling localhost Ollama
    messages = [
        {"role": "system", "content": "You are friendly."},
        {"role": "user", "content": user_input}
    ]

    # Mock response
    r_status = 200
    r_text = "Hello there! How can I help you today?"

    st.subheader("Bot response")
    st.write(r_text)

# Simple order form
st.subheader("Place an Order")
with st.form("order_form"):
    name = st.text_input("Your Name")
    item = st.selectbox("Select Item", [m["item"] for m in menu])
    quantity = st.number_input("Quantity", min_value=1, max_value=20, value=1)
    submitted = st.form_submit_button("Order Now")
    if submitted:
        st.success(f"Thank you {name}! Your order of {quantity} x {item} has been received.")
