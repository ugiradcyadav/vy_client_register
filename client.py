"""
V.Y. Tech — Client Registration Portal
Run with: streamlit run vy_client_register.py
"""

import streamlit as st
import json
import os
from datetime import datetime

CLIENTS_FILE = "vy_clients.json"
IB_VANTAGE_LINK = "https://www.vantagemarkets.com/open-live-account/?affid=MjMxNDgzOTU=&invitecode=u0vkGliE"
IB_DISCOUNT_PERCENT = 15
WALLET_ADDRESS = "2tVBtgRjSeWePCniFXnjoKbdzvnmKKBiqciXUTGnTT2r"

PLANS = {
    "Trial":     {"price": 0,   "days": 7,   "label": "7-day Free Trial — FREE"},
    "Monthly":   {"price": 49,  "days": 30,  "label": "Monthly — $49/month"},
    "Quarterly": {"price": 129, "days": 90,  "label": "Quarterly — $129 (save 12%)"},
    "Annual":    {"price": 399, "days": 365, "label": "Annual — $399 (save 32%)"},
    "Lifetime":  {"price": 999, "days": 36500, "label": "Lifetime — $999 one-time"},
}

def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        return []
    with open(CLIENTS_FILE, "r") as f:
        return json.load(f)

def save_clients(data):
    with open(CLIENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def already_registered(email):
    clients = load_clients()
    return any(c.get("email", "").lower() == email.lower() for c in clients)

# ─────────────────────────────────────────────────────────────
# CSS (Pure White Theme)
# ─────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    *, html, body, .stApp, .main { font-family: 'Inter', sans-serif !important; }
    html, body, .stApp, .main    { background-color: #ffffff !important; color: #111827 !important; }
    .block-container              { padding-top: 0 !important; max-width: 680px !important; margin: 0 auto !important; }
    
    /* Button Styling */
    .stButton > button            { background: linear-gradient(135deg, #0050bb 0%, #6018cc 100%) !important; 
                                    color: #fff !important; border: none !important; border-radius: 8px !important; 
                                    font-weight: 600 !important; transition: all .2s !important; font-size: 14px !important; }
    .stButton > button:hover      { filter: brightness(1.15) !important; transform: translateY(-1px) !important; box-shadow: 0 4px 12px rgba(0,80,187,0.2) !important; }
    
    /* Input Fields Styling */
    .stTextInput input, .stNumberInput input, .stTextArea textarea { 
        background: #f9fafb !important; border: 1px solid #d1d5db !important; 
        color: #111827 !important; border-radius: 8px !important; font-size: 14px !important; }
    .stSelectbox [data-baseweb="select"] > div { 
        background: #f9fafb !important; border-color: #d1d5db !important; color: #111827 !important; }
    
    /* Text Colors */
    .stRadio > div > label        { color: #374151 !important; }
    .stCheckbox > label           { color: #374151 !important; font-size: 14px !important; }
    p, div, span, label           { color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="V.Y. Tech — Join Platform", page_icon="📈", layout="centered")
inject_css()

# HERO
st.markdown("""
<div style="text-align:center;padding:48px 20px 24px;">
    <div style="font-size:38px;font-weight:900;letter-spacing:7px;
                background:linear-gradient(135deg,#0050bb 0%,#7b2ff7 100%);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        V.Y. TECH
    </div>
    <div style="color:#6b7280;font-size:10px;letter-spacing:4px;text-transform:uppercase;margin-top:4px;">
        Institutional AI Trading Platform
    </div>
    <div style="color:#4b5563;font-size:14px;margin-top:12px;line-height:1.6;">
        Subscribe to access the <b style="color:#0050bb;">Omega AI Platform</b> — RF + LSTM ensemble<br>
        signals for Gold, Forex & more, directly in MetaTrader 5.
    </div>
</div>
""", unsafe_allow_html=True)

# PRICING CARDS
st.markdown("""
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:24px;">
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:16px;text-align:center;box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="color:#6b7280;font-size:10px;letter-spacing:2px;text-transform:uppercase;">Monthly</div>
        <div style="font-size:26px;font-weight:900;color:#111827;margin:6px 0;">$49</div>
        <div style="color:#6b7280;font-size:11px;">30 days access</div>
    </div>
    <div style="background:#f0f9ff;border:2px solid #0050bb;
                border-radius:12px;padding:16px;text-align:center;position:relative;box-shadow: 0 4px 6px rgba(0,80,187,0.1);">
        <div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);
                    background:linear-gradient(135deg,#0050bb,#6018cc);
                    color:#fff;font-size:9px;font-weight:700;padding:3px 10px;border-radius:20px;
                    letter-spacing:1px;white-space:nowrap;">MOST POPULAR</div>
        <div style="color:#0369a1;font-size:10px;letter-spacing:2px;text-transform:uppercase;">Quarterly</div>
        <div style="font-size:26px;font-weight:900;color:#0f172a;margin:6px 0;">$129</div>
        <div style="color:#0284c7;font-size:11px;">90 days · save 12%</div>
    </div>
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:16px;text-align:center;box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="color:#6b7280;font-size:10px;letter-spacing:2px;text-transform:uppercase;">Annual</div>
        <div style="font-size:26px;font-weight:900;color:#111827;margin:6px 0;">$399</div>
        <div style="color:#6b7280;font-size:11px;">365 days · save 32%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# IB Banner
st.markdown(f"""
<div style="background:#fdf4ff;border:1px solid #f5d0fe;
            border-radius:12px;padding:14px 18px;margin-bottom:20px;
            display:flex;align-items:center;justify-content:space-between;">
    <div>
        <div style="color:#86198f;font-size:13px;font-weight:600;margin-bottom:3px;">
            🤝 Vantage IB Partner Discount
        </div>
        <div style="color:#a21caf;font-size:12px;">
            Open a Vantage account via our partner link and get
            <b style="color:#701a75;">{IB_DISCOUNT_PERCENT}% off</b> any subscription plan.
        </div>
    </div>
    <a href="{IB_VANTAGE_LINK}" target="_blank"
       style="background:linear-gradient(135deg,#e8430a,#f07020);color:#fff;padding:8px 16px;
              border-radius:8px;font-size:12px;font-weight:600;text-decoration:none;
              white-space:nowrap;margin-left:16px;box-shadow: 0 2px 4px rgba(232,67,10,0.2);">
        Open Vantage →
    </a>
</div>
""", unsafe_allow_html=True)

# ─── REGISTRATION FORM ────────────────────────────────────────

st.markdown("""
<div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;padding:28px;margin-bottom:20px;box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
    <div style="color:#111827;font-size:16px;font-weight:700;margin-bottom:4px;">📋 Registration & Payment Form</div>
    <div style="color:#4b5563;font-size:12px;">Fill in your details. After submitting, complete your USDT payment to get your license key.</div>
</div>
""", unsafe_allow_html=True)

with st.form("registration_form", clear_on_submit=False):
    st.markdown("##### 👤 Personal Details")
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        f_name  = st.text_input("Full Name *", placeholder="Ahmed Khan")
        f_email = st.text_input("Email Address *", placeholder="ahmed@email.com")
    with f_col2:
        f_phone   = st.text_input("WhatsApp Number *", placeholder="+92-300-0000000")
        f_country = st.text_input("Country", placeholder="Pakistan")

    st.markdown("---")
    st.markdown("##### 📊 Trading Details")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        f_broker = st.text_input("Broker Name *", placeholder="e.g. Vantage, XM, ICMarkets")
        f_acc_id = st.text_input("MT5 Account Number", placeholder="Your broker account number")
    with b_col2:
        f_plan  = st.selectbox("Subscription Plan *", list(PLANS.keys()), 
                               format_func=lambda x: PLANS[x]["label"], index=1)
        f_exp   = st.selectbox("Trading Experience", ["Beginner (<1 year)", "Intermediate (1-3 years)", "Advanced (3+ years)", "Professional"])

    st.markdown("---")
    st.markdown("##### 🤝 IB Partner Discount")
    f_ib = st.checkbox(
        f"I opened my trading account via the V.Y. Tech / Vantage IB link — apply {IB_DISCOUNT_PERCENT}% discount",
        value=False
    )
    
    st.markdown("##### 💳 Payment Method")
    st.info("Payment is accepted via **USDT (Solana Network)**. Address will be provided upon submission.")

    f_notes = st.text_area("Anything else? (optional)", placeholder="Questions, special requests, referral name...")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🚀 Submit & Proceed to Payment", use_container_width=True, type="primary")

if submitted:
    # Validation
    errors = []
    if not f_name.strip():   errors.append("Full name is required.")
    if not f_email.strip():  errors.append("Email is required.")
    if "@" not in f_email:   errors.append("Please enter a valid email address.")
    if not f_phone.strip():  errors.append("WhatsApp number is required.")
    if not f_broker.strip(): errors.append("Broker name is required.")

    if errors:
        for err in errors:
            st.error(f"❌ {err}")
    elif already_registered(f_email.strip()):
        st.warning("""
        ⚠️ This email is already registered. 
        If you haven't received your license key yet, please contact V.Y. Tech support via WhatsApp.
        """)
    else:
        clients = load_clients()
        
        # Calculate final price
        base_price = PLANS[f_plan]["price"]
        final_price = round(base_price * (1 - IB_DISCOUNT_PERCENT / 100), 2) if f_ib else base_price

        clients.append({
            "name":         f_name.strip(),
            "email":        f_email.strip().lower(),
            "phone":        f_phone.strip(),
            "country":      f_country.strip(),
            "broker":       f_broker.strip(),
            "account_id":   f_acc_id.strip(),
            "plan":         f_plan,
            "amount_due":   final_price,
            "experience":   f_exp,
            "ib_partner":   f_ib,
            "notes":        f_notes.strip(),
            "status":       "pending_payment",
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        save_clients(clients)

        # Success Message
        st.success(f"✅ Registration Saved! Hello **{f_name}**, your request for the **{f_plan}** plan is registered.")
        
        # Light Green Payment Box HTML
        html_success = f"""
        <div style="background:#f0fdf4; border:2px solid #10b981; border-radius:12px; padding:20px; text-align:center; margin-top:10px; margin-bottom:10px;">
            <div style="color:#047857; font-size:16px; font-weight:800; margin-bottom:15px;">
                PLEASE COMPLETE YOUR PAYMENT
            </div>
            <div style="color:#6b7280; font-size:12px; text-transform:uppercase; letter-spacing:1px;">Amount to Send</div>
            <div style="color:#111827; font-size:32px; font-weight:900; margin:5px 0;">${final_price} USDT</div>
            <div style="color:#6b7280; font-size:12px; text-transform:uppercase; letter-spacing:1px; margin-top:16px;">Network</div>
            <div style="color:#0050bb; font-size:16px; font-weight:700;">Solana (SOL)</div>
            <div style="color:#6b7280; font-size:12px; text-transform:uppercase; letter-spacing:1px; margin-top:16px;">Wallet Address (Click icon on right to copy) 👇</div>
        </div>
        """
        st.markdown(html_success, unsafe_allow_html=True)

        # In-built code box with automatic copy button
        st.code(WALLET_ADDRESS, language="text")

        st.info("ℹ️ After sending the payment, please share the screenshot/TxID on our WhatsApp support. Your license key will be sent within 24 hours.")

# FEATURES
st.markdown("""
<div style="margin-top:32px;">
    <div style="color:#6b7280; font-size:11px; letter-spacing:3px; text-transform:uppercase; text-align:center; margin-bottom:16px;">
        What You Get
    </div>
    <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:10px;">
        <div style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:14px;">
            <div style="color:#0050bb; font-size:13px; font-weight:700; margin-bottom:4px;">🧠 RF + LSTM AI Ensemble</div>
            <div style="color:#4b5563; font-size:12px;">Dual AI model on 10,080 candle history for high-accuracy signals</div>
        </div>
        <div style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:14px;">
            <div style="color:#0050bb; font-size:13px; font-weight:700; margin-bottom:4px;">⚡ Auto + Signal Modes</div>
            <div style="color:#4b5563; font-size:12px;">Choose between manual signals-only or fully automated trading</div>
        </div>
        <div style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:14px;">
            <div style="color:#0050bb; font-size:13px; font-weight:700; margin-bottom:4px;">🛡️ Smart Risk Management</div>
            <div style="color:#4b5563; font-size:12px;">Auto SL, Break-Even, Trailing Stop, max trade limits</div>
        </div>
        <div style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:14px;">
            <div style="color:#0050bb; font-size:13px; font-weight:700; margin-bottom:4px;">📅 Economic Calendar</div>
            <div style="color:#4b5563; font-size:12px;">Live MT5 calendar — NFP, CPI, speeches, no extra API needed</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top:36px; padding-top:16px; border-top:1px solid #e5e7eb; font-size:11px; color:#6b7280;">
    © 2026 <span style="color:#111827; font-weight:700;">V.Y. TECH</span> · All Rights Reserved<br>
    ⚠️ Trading involves significant risk. AI signals are not financial advice.
</div>
""", unsafe_allow_html=True)
