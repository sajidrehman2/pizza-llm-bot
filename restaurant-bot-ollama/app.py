# app.py
import streamlit as st

st.set_page_config(page_title="Sajid's Pizzeria", page_icon="🍕", layout="centered")

st.title("🍕 Sajid's Pizzeria")
st.subheader("Delicious food delivered with AI-powered ordering")

# Menu
st.markdown("""
📖 **Today's Menu**

**🍕 PIZZAS:**
- Margherita (S: $12.99, M: $16.99, L: $20.99)
- Pepperoni (S: $14.99, M: $18.99, L: $22.99)
- Supreme (S: $17.99, M: $21.99, L: $25.99)
- Vegetarian (S: $15.99, M: $19.99, L: $23.99)

**🥓 TOPPINGS:**
- Extra Cheese: $2.50
- Mushrooms: $2.00
- Pepperoni: $3.00
- Sausage: $3.00
- Olives: $2.00
- Bell Peppers: $2.00

**🍟 SIDES:**
- Garlic Bread: $5.99
- Chicken Wings (6pc: $8.99, 12pc: $15.99)
- Caesar Salad: $7.99
- Fries (S: $3.99, L: $5.99)

**🥤 DRINKS:**
- Coca Cola (S: $2.99, M: $3.99, L: $4.99)
- Sprite (S: $2.99, M: $3.99, L: $4.99)
- Water: $1.99
- Juice (S: $3.99, M: $4.99)
""")

st.markdown("💬 **Order Assistant**")
st.write("Welcome to Sajid's Pizzeria! I'm your AI ordering assistant. 😊")

# User input
user_input = st.text_input("Tell me what you'd like to order... 🍕")

if user_input:
    # Mock AI response
    response_text = f"Hi! You said: '{user_input}'. Your order is being processed! 🍕"
    st.success(response_text)

st.markdown("---")
st.markdown("🍕 **Sajid's Pizzeria - Powered by AI | Made with ❤️ and Streamlit**")
st.markdown("Tip: Be specific about sizes and quantities for accurate pricing!")

