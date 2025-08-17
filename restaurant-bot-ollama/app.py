# Enhanced Streamlit restaurant ordering bot (Ollama local). Save file as UTF-8.
import json
import os
import re
import requests
import streamlit as st
import pandas as pd
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# ---------- Config ----------
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = "gemma:2b"  # small model
MENU_FILE = "menu.json"
ORDERS_FILE = "orders.csv"

# ---------- Custom CSS for styling ----------
def load_css():
    st.markdown("""
    <style>
    /* Main app styling */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Custom header styling */
    .custom-header {
        background: linear-gradient(135deg, #ff6b6b, #ffa500, #ff1744);
        padding: 2rem 1rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
    }
    
    .custom-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: 700;
    }
    
    .custom-header p {
        color: white;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Menu card styling */
    .menu-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        color: white;
    }
    
    .menu-card h3 {
        color: white;
        margin-top: 0;
        font-size: 1.5rem;
        text-align: center;
    }
    
    .menu-content {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Chat message styling */
    .chat-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
    }
    
    .chat-container h3 {
        color: white;
        text-align: center;
        margin-top: 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Error message styling */
    .success-card {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .error-card {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: #4CAF50;
        animation: pulse 2s infinite;
    }
    
    .status-offline {
        background-color: #f44336;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Metrics styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- UI Components ----------
def render_custom_header():
    st.markdown("""
    <div class="custom-header">
        <h1>🍕 Sajid's Pizzeria</h1>
        <p>Delicious food delivered with AI-powered ordering</p>
    </div>
    """, unsafe_allow_html=True)

def render_connection_status():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            status_html = '<span class="status-indicator status-online"></span>Ollama Connected'
            status_color = "success"
        else:
            status_html = '<span class="status-indicator status-offline"></span>Ollama Disconnected'
            status_color = "error"
    except:
        status_html = '<span class="status-indicator status-offline"></span>Ollama Disconnected'
        status_color = "error"
    
    st.sidebar.markdown(f'**Connection Status:** {status_html}', unsafe_allow_html=True)

def render_menu_card(menu_text):
    st.markdown("""
    <div class="menu-card">
        <h3>📖 Today's Menu</h3>
        <div class="menu-content">
    """, unsafe_allow_html=True)
    
    if menu_text:
        # Format menu text with better styling
        formatted_menu = menu_text.replace("🍕", "🍕").replace("🥓", "🥓").replace("🍟", "🍟").replace("🥤", "🥤")
        st.markdown(f"```\n{formatted_menu}\n```")
    else:
        st.warning("No menu loaded. Please create menu.json file.")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_order_summary_card(total, line_items):
    st.markdown('<div class="success-card">', unsafe_allow_html=True)
    st.markdown(f'### 🧾 Order Summary - Total: ${total:.2f}')
    if line_items:
        df = pd.DataFrame(line_items)
        st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Helpers: menu file ----------
def load_menu() -> Dict[str, Any]:
    if not os.path.exists(MENU_FILE):
        return create_sample_menu()
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load {MENU_FILE}: {e}")
        return {}

def create_sample_menu():
    """Create a sample menu if none exists"""
    sample_menu = {
        "pizzas": {
            "margherita": {"S": 12.99, "M": 16.99, "L": 20.99},
            "pepperoni": {"S": 14.99, "M": 18.99, "L": 22.99},
            "supreme": {"S": 17.99, "M": 21.99, "L": 25.99},
            "vegetarian": {"S": 15.99, "M": 19.99, "L": 23.99}
        },
        "toppings": {
            "extra cheese": 2.50,
            "mushrooms": 2.00,
            "pepperoni": 3.00,
            "sausage": 3.00,
            "olives": 2.00,
            "bell peppers": 2.00
        },
        "drinks": {
            "coca cola": {"S": 2.99, "M": 3.99, "L": 4.99},
            "sprite": {"S": 2.99, "M": 3.99, "L": 4.99},
            "water": 1.99,
            "juice": {"S": 3.99, "M": 4.99}
        },
        "sides": {
            "garlic bread": 5.99,
            "chicken wings": {"6pc": 8.99, "12pc": 15.99},
            "caesar salad": 7.99,
            "fries": {"S": 3.99, "L": 5.99}
        }
    }
    
    try:
        with open(MENU_FILE, "w", encoding="utf-8") as f:
            json.dump(sample_menu, f, indent=2)
        st.info("Created sample menu.json file. You can customize it!")
    except Exception as e:
        st.error(f"Could not create sample menu: {e}")
    
    return sample_menu

def menu_to_text(menu: Dict[str, Any]) -> str:
    if not menu: return "No menu available."
    out_lines: List[str] = []

    pizzas = menu.get("pizzas", {})
    if pizzas:
        out_lines.append("🍕 PIZZAS:")
        for name, sizes in pizzas.items():
            try:
                sizes_text = ", ".join([f"{sz}: ${float(price):.2f}" for sz, price in sizes.items()])
            except Exception:
                sizes_text = ", ".join([f"{sz}: {price}" for sz, price in sizes.items()])
            out_lines.append(f"   • {name.title()} ({sizes_text})")
        out_lines.append("")

    toppings = menu.get("toppings", {})
    if toppings:
        out_lines.append("🥓 TOPPINGS:")
        for name, price in toppings.items():
            try:
                out_lines.append(f"   • {name.title()}: ${float(price):.2f}")
            except Exception:
                out_lines.append(f"   • {name.title()}: {price}")
        out_lines.append("")

    sides = menu.get("sides", {})
    if sides:
        out_lines.append("🍟 SIDES:")
        for name, sizes in sides.items():
            if isinstance(sizes, dict):
                sizes_text = ", ".join([f"{sz}: ${float(price):.2f}" for sz, price in sizes.items()])
                out_lines.append(f"   • {name.title()} ({sizes_text})")
            else:
                out_lines.append(f"   • {name.title()}: ${float(sizes):.2f}")
        out_lines.append("")

    drinks = menu.get("drinks", {})
    if drinks:
        out_lines.append("🥤 DRINKS:")
        for name, sizes in drinks.items():
            if isinstance(sizes, dict):
                sizes_text = ", ".join([f"{sz}: ${float(price):.2f}" for sz, price in sizes.items()])
                out_lines.append(f"   • {name.title()} ({sizes_text})")
            else:
                out_lines.append(f"   • {name.title()}: ${float(sizes):.2f}")
        out_lines.append("")

    return "\n".join(out_lines).strip()

# ---------- Helpers: pricing ----------
def get_price_for_item(table: Dict[str, Any], name: Optional[str], size: Optional[str] = None) -> float:
    if not name: return 0.0
    name_key = name.lower().strip()
    if not table or name_key not in table: return 0.0
    entry = table[name_key]
    if isinstance(entry, dict):
        if size:
            size_key = size.upper().strip()
            val = entry.get(size_key)
            if val is None:
                for k, v in entry.items():
                    if str(k).upper().strip() == size_key:
                        return float(v)
                return 0.0
            return float(val)
        if "REG" in entry:
            return float(entry["REG"])
        for v in entry.values():
            try: return float(v)
            except: continue
        return 0.0
    try: return float(entry)
    except: return 0.0

def calculate_total_from_summary(order: Dict[str, Any], menu: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
    line_items: List[Dict[str, Any]] = []
    total = 0.0

    for p in order.get("pizzas", []):
        name = p.get("name")
        size = p.get("size")
        qty = int(p.get("qty", p.get("quantity", 1)))
        price = get_price_for_item(menu.get("pizzas", {}), name, size)
        line_total = round(price * qty, 2)
        total += line_total
        line_items.append({"type": "🍕 Pizza", "name": name.title(), "size": size, "qty": qty, "unit_price": f"${price:.2f}", "total": f"${line_total:.2f}"})

    for t in order.get("toppings", []):
        name = t.get("name")
        qty = int(t.get("qty", t.get("quantity", 1)))
        price = get_price_for_item(menu.get("toppings", {}), name, None)
        line_total = round(price * qty, 2)
        total += line_total
        line_items.append({"type": "🥓 Topping", "name": name.title(), "size": "-", "qty": qty, "unit_price": f"${price:.2f}", "total": f"${line_total:.2f}"})

    for d in order.get("drinks", []):
        name = d.get("name")
        size = d.get("size")
        qty = int(d.get("qty", d.get("quantity", 1)))
        price = get_price_for_item(menu.get("drinks", {}), name, size)
        line_total = round(price * qty, 2)
        total += line_total
        line_items.append({"type": "🥤 Drink", "name": name.title(), "size": size or "-", "qty": qty, "unit_price": f"${price:.2f}", "total": f"${line_total:.2f}"})

    for s in order.get("sides", []):
        name = s.get("name")
        size = s.get("size")
        qty = int(s.get("qty", s.get("quantity", 1)))
        price = get_price_for_item(menu.get("sides", {}), name, size)
        line_total = round(price * qty, 2)
        total += line_total
        line_items.append({"type": "🍟 Side", "name": name.title(), "size": size or "-", "qty": qty, "unit_price": f"${price:.2f}", "total": f"${line_total:.2f}"})

    return round(total, 2), line_items

# ---------- Helpers: Ollama communication ----------
def call_ollama(model: str, messages: List[Dict[str, str]], timeout: int = 120) -> str:
    url = f"{OLLAMA_URL}/api/chat"
    payload = {"model": model, "messages": messages, "stream": False}
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        return "ERROR: Could not connect to Ollama. Is Ollama running? Try: ollama --version"
    except requests.exceptions.HTTPError as e:
        return f"ERROR calling Ollama: {r.status_code} {r.text}"
    except Exception as e:
        return f"ERROR calling Ollama: {e}"

    try: data = r.json()
    except: return r.text or "(no response from model)"

    if isinstance(data, dict):
        if "message" in data and isinstance(data["message"], dict) and "content" in data["message"]:
            return str(data["message"]["content"]).strip()
        if "content" in data: return str(data["content"]).strip()
        if "response" in data: return str(data["response"]).strip()
    return json.dumps(data)

# ---------- Helpers: JSON extraction ----------
def extract_json_from_text(text: str) -> Optional[str]:
    if not text: return None
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL|re.IGNORECASE)
    if fence_match:
        candidate = fence_match.group(1).strip()
        try: json.loads(candidate); return candidate
        except: text = candidate
    try: json.loads(text); return text
    except: pass
    first = text.find("{"); last = text.rfind("}")
    if first != -1 and last != -1 and last > first:
        candidate = text[first:last+1]
        try: json.loads(candidate); return candidate
        except: pass
    return None

# ---------- Chat system message ----------
def system_message(menu_text: str) -> Dict[str, str]:
    return {"role": "system", "content": (
        "You are OrderBot, a friendly AI assistant for Sajid's Pizzeria! 🍕\n"
        "- Greet customers warmly and help them place orders\n"
        "- Be enthusiastic about the food and make recommendations\n"
        "- Always clarify sizes, quantities, and any special requests\n"
        "- Ask about pickup or delivery, and collect address if needed\n"
        "- Summarize orders clearly before finalizing\n"
        "- Only offer items from our menu below\n"
        "- Be helpful, friendly, and make the ordering experience enjoyable!\n\n"
        f"🍽️ SAJID'S PIZZERIA MENU:\n{menu_text}\n\n"
        "Remember: Great customer service makes great pizza even better! 😊"
    )}

JSON_ORDER_SCHEMA_INSTRUCTION = (
    "Please create a JSON summary of the customer's complete order using this exact format:\n"
    "{\n"
    ' "pizzas": [{"name": "pizza_name", "size": "S/M/L", "qty": number}],\n'
    ' "toppings": [{"name": "topping_name", "qty": number, "applies_to": "all"}],\n'
    ' "drinks": [{"name": "drink_name", "size": "S/M/L", "qty": number}],\n'
    ' "sides": [{"name": "side_name", "size": "size_if_applicable", "qty": number}],\n'
    ' "delivery_method": "pickup" or "delivery",\n'
    ' "address": "customer_address_if_delivery" or null,\n'
    ' "notes": "any_special_instructions" or null\n'
    "}\n"
    "Return ONLY the JSON - no other text or commentary."
)

# ---------- Main Streamlit App ----------
def main():
    st.set_page_config(
        page_title="Sajid's Pizzeria - AI Ordering",
        page_icon="🍕",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_css()
    
    # Custom header
    render_custom_header()
    
    # Load menu
    menu = load_menu()
    menu_text = menu_to_text(menu)

    # Sidebar configuration
    st.sidebar.title("⚙️ Restaurant Settings")
    render_connection_status()
    
    st.sidebar.markdown("---")
    model_choice = st.sidebar.selectbox(
        "🤖 AI Model", 
        [DEFAULT_MODEL, "llama3", "mistral", "phi3"], 
        index=0,
        help="Choose the AI model for order processing"
    )
    
    st.sidebar.info(f"📡 Ollama URL: {OLLAMA_URL}")
    st.sidebar.markdown("Make sure Ollama is running before taking orders!")
    
    if st.sidebar.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.pop("messages", None)
        st.rerun()

    # Main layout with columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_menu_card(menu_text)
    
    with col2:
        # Order statistics
        if os.path.exists(ORDERS_FILE):
            try:
                orders_df = pd.read_csv(ORDERS_FILE)
                total_orders = len(orders_df['timestamp'].unique())
                total_revenue = orders_df['total'].str.replace('$', '').astype(float).sum() if 'total' in orders_df.columns else 0
                
                st.markdown("### 📊 Today's Stats")
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Total Orders", total_orders)
                with metric_col2:
                    st.metric("Revenue", f"${total_revenue:.2f}")
            except:
                pass

    # Chat interface
    st.markdown('<div class="chat-container"><h3>💬 Order Assistant</h3></div>', unsafe_allow_html=True)

    # Initialize session
    if "messages" not in st.session_state:
        st.session_state.messages = [
            system_message(menu_text),
            {"role": "assistant", "content": "🍕 Welcome to Sajid's Pizzeria! I'm your AI ordering assistant. What delicious pizza can I help you with today? Our most popular items are the Supreme Pizza and our famous garlic bread! 😊"}
        ]

    # Display chat messages
    for m in st.session_state.messages:
        if m.get("role") == "system": continue
        with st.chat_message(m.get("role")):
            st.markdown(m.get("content"))

    # User input
    user_input = st.chat_input("Tell me what you'd like to order... 🍕")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Processing your order..."):
                messages_for_model = st.session_state.messages.copy()
                if messages_for_model and messages_for_model[0].get("role") != "system":
                    messages_for_model.insert(0, system_message(menu_text))
                reply_text = call_ollama(model_choice, messages_for_model)
                if not reply_text:
                    reply_text = "⚠️ Sorry, I'm having trouble connecting to our ordering system. Please try again!"
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})

    st.markdown("---")

    # Action buttons
    button_col1, button_col2, button_col3 = st.columns(3)
    
    with button_col1:
        if st.button("🧾 Calculate Order Total", use_container_width=True):
            messages_for_model = st.session_state.messages.copy()
            if messages_for_model and messages_for_model[0].get("role") != "system":
                messages_for_model.insert(0, system_message(menu_text))
            messages_for_model.append({"role": "user", "content": JSON_ORDER_SCHEMA_INSTRUCTION})
            
            with st.spinner("📋 Preparing your order summary..."):
                raw = call_ollama(model_choice, messages_for_model)
                if not raw:
                    st.error("❌ Could not process order. Please check connection.")
                else:
                    extracted = extract_json_from_text(raw)
                    if not extracted:
                        st.error("❌ Could not generate order summary. Please try again.")
                        with st.expander("Debug Info"):
                            st.code(raw)
                    else:
                        try:
                            order_summary = json.loads(extracted)
                            total, lines = calculate_total_from_summary(order_summary, menu)
                            
                            render_order_summary_card(total, lines)
                            
                            # Save order
                            if lines:
                                rows = []
                                ts = int(time.time())
                                for l in lines:
                                    row = {
                                        "timestamp": ts,
                                        "delivery_method": order_summary.get("delivery_method"),
                                        "address": order_summary.get("address")
                                    }
                                    # Clean the line item data
                                    clean_line = {k: str(v).replace('$', '') if k in ['unit_price', 'total'] else v 
                                                for k, v in l.items()}
                                    row.update(clean_line)
                                    rows.append(row)
                                
                                df_rows = pd.DataFrame(rows)
                                if os.path.exists(ORDERS_FILE):
                                    df_prev = pd.read_csv(ORDERS_FILE)
                                    df_out = pd.concat([df_prev, df_rows], ignore_index=True)
                                else:
                                    df_out = df_rows
                                df_out.to_csv(ORDERS_FILE, index=False)
                                st.success("✅ Order saved successfully!")
                        except Exception as e:
                            st.error("❌ Error processing order summary")
                            st.exception(e)

    with button_col2:
        if st.button("🧹 New Order", use_container_width=True):
            sys_msg = system_message(menu_text)
            st.session_state.messages = [
                sys_msg,
                {"role": "assistant", "content": "🍕 Welcome to Sajid's Pizzeria! I'm ready to take your next order. What can I get started for you today? 😊"}
            ]
            st.rerun()
    
    with button_col3:
        if st.button("📊 View Orders", use_container_width=True):
            if os.path.exists(ORDERS_FILE):
                try:
                    df = pd.read_csv(ORDERS_FILE)
                    st.markdown("### 📋 Recent Orders")
                    st.dataframe(df.tail(10), use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading orders: {e}")
            else:
                st.info("No orders found yet.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🍕 Sajid's Pizzeria - Powered by AI | Made with ❤️ and Streamlit</p>
        <p><em>Tip: Be specific about sizes and quantities for accurate pricing!</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
