"""
V.Y. Tech — Client Registration Portal
Run with: streamlit run vy_client_register.py
"""

import streamlit as st
import json
import os
import time
import requests
from datetime import datetime

# --- CONFIGURATION & CONSTANTS ---
CLIENTS_FILE = "vy_clients.json"
IB_VANTAGE_LINK = "https://www.vantagemarkets.com/open-live-account/?affid=MjMxNDgzOTU=&invitecode=u0vkGliE"
IB_DISCOUNT_PERCENT = 15

# YAHAN APNI HELIUS API KEY DAALEIN 👇
HELIUS_API_KEY = "be1c7613-5cb4-492a-afc3-c07c3443b923" 

WALLET_ADDRESS = "2tVBtgRjSeWePCniFXnjoKbdzvnmKKBiqciXUTGnTT2r"
USDT_MINT_ADDRESS = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB" # Official Solana USDT Address

PLANS = {
    "Trial":      {"price": 0,    "days": 1,   "label": "1-day Free Trial"},
    "Weekly":      {"price": 10,    "days": 7,   "label": "7-day — $10"},
    "Monthly":   {"price": 49,  "days": 30,  "label": "Monthly — $49/month"},
    "Quarterly": {"price": 129, "days": 90,  "label": "Quarterly — $129 (save 12%)"},
    "Annual":    {"price": 399, "days": 365, "label": "Annual — $399 (save 32%)"},
    "Lifetime":  {"price": 999, "days": 36500, "label": "Lifetime — $999 one-time"},
}

# --- SESSION STATE ---
if 'step' not in st.session_state:
    st.session_state.step = 'registration'
if 'current_client_email' not in st.session_state:
    st.session_state.current_client_email = ''
if 'amount_due' not in st.session_state:
    st.session_state.amount_due = 0

# --- DATABASE FUNCTIONS (JSON) ---
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

def update_client_status(email, tx_id, status="paid"):
    clients = load_clients()
    for c in clients:
        if c.get("email") == email:
            c["status"] = status
            c["tx_id"] = tx_id
            c["payment_verified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    save_clients(clients)

# --- CRYPTO VERIFICATION FUNCTION ---
def verify_solana_transaction(tx_id, expected_amount):
    tx_id = tx_id.strip()
    
    # Agar API key set nahi ki hai, toh error na aaye isliye dummy verify karega
    if HELIUS_API_KEY == "YAHAN_APNI_HELIUS_API_KEY_DAALEIN":
        time.sleep(2)
        return True, "Mock Verified (Warning: API Key set nahi hai, yeh real verification nahi hai)"

    url = f"https://api.helius.xyz/v0/transactions/?api-key={HELIUS_API_KEY}"
    payload = {"transactions": [tx_id]}
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code != 200:
            return False, f"API Error ({response.status_code}). Please check your Helius API Key."
            
        data = response.json()
        if not data:
            return False, "Transaction ID not found. Agar abhi payment ki hai, toh 30 seconds wait karke dobara try karein."
            
        tx_data = data[0]
        
        # Check 1: Did the transaction fail on the blockchain?
        if tx_data.get("transactionError"):
            return False, "Yeh transaction blockchain par fail ho chuki hai."
            
        # Check 2: Find USDT transfer to our wallet
        token_transfers = tx_data.get("tokenTransfers", [])
        for transfer in token_transfers:
            # Match Mint (USDT) and Receiver (Your Wallet)
            if transfer.get("mint") == USDT_MINT_ADDRESS and transfer.get("toUserAccount") == WALLET_ADDRESS:
                amount_received = transfer.get("tokenAmount", 0)
                
                # Check 3: Is the amount correct?
                if float(amount_received) >= float(expected_amount):
                    return True, f"Payment Verified! {amount_received} USDT Received."
                else:
                    return False, f"Amount Mismatch! Expected ${expected_amount} but received ${amount_received}."
                    
        return False, "Transaction valid hai, par isme aapke wallet mein USDT receive nahi hua."
        
    except Exception as e:
        return False, f"System Error: {str(e)}"

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
    
    .stButton > button            { background: linear-gradient(135deg, #0050bb 0%, #6018cc 100%) !important; 
                                    color: #fff !important; border: none !important; border-radius: 8px !important; 
                                    font-weight: 600 !important; transition: all .2s !important; font-size: 14px !important; }
    .stButton > button:hover      { filter: brightness(1.15) !important; transform: translateY(-1px) !important; box-shadow: 0 4px 12px rgba(0,80,187,0.2) !important; }
    
    .stTextInput input, .stNumberInput input, .stTextArea textarea { 
        background: #f9fafb !important; border: 1px solid #d1d5db !important; 
        color: #111827 !important; border-radius: 8px !important; font-size: 14px !important; }
    .stSelectbox [data-baseweb="select"] > div { background: #f9fafb !important; border-color: #d1d5db !important; color: #111827 !important; }
    .stRadio > div > label        { color: #374151 !important; }
    .stCheckbox > label           { color: #374151 !important; font-size: 14px !important; }
    p, div, span, label           { color: #111827; }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="V.Y. Tech — Join Platform", page_icon="📈", layout="centered")
inject_css()

# HERO SECTION
st.markdown("""
<div style="text-align:center;padding:48px 20px 24px;">
    <div style="font-size:38px;font-weight:900;letter-spacing:7px; background:linear-gradient(135deg,#0050bb 0%,#7b2ff7 100%); -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        V.Y. TECH
    </div>
    <div style="color:#6b7280;font-size:10px;letter-spacing:4px;text-transform:uppercase;margin-top:4px;">Institutional AI Trading Platform</div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# STEP 1: REGISTRATION FORM
# =====================================================================
if st.session_state.step == 'registration':
    
    st.markdown("""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;padding:28px;margin-bottom:20px;box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
        <div style="color:#111827;font-size:16px;font-weight:700;margin-bottom:4px;">📋 Step 1: Registration Details</div>
        <div style="color:#4b5563;font-size:12px;">Fill in your details. After submitting, you will be redirected to the secure payment portal.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("registration_form"):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            f_name  = st.text_input("Full Name *", placeholder="Ahmed Khan")
            f_email = st.text_input("Email Address *", placeholder="ahmed@email.com")
        with f_col2:
            f_phone   = st.text_input("WhatsApp Number *", placeholder="+92-300-0000000")
            f_country = st.text_input("Country", placeholder="Pakistan")

        b_col1, b_col2 = st.columns(2)
        with b_col1:
            f_broker = st.text_input("Broker Name *", placeholder="e.g. Vantage, XM")
            f_acc_id = st.text_input("MT5 Account Number", placeholder="Your broker account number")
        with b_col2:
            f_plan  = st.selectbox("Subscription Plan *", list(PLANS.keys()), format_func=lambda x: PLANS[x]["label"], index=1)
            f_exp   = st.selectbox("Trading Experience", ["Beginner", "Intermediate", "Advanced", "Professional"])

        st.markdown("---")
        f_ib = st.checkbox(f"Apply {IB_DISCOUNT_PERCENT}% IB Partner Discount (if account opened via our link)", value=False)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Proceed to Payment ➔", use_container_width=True, type="primary")

    if submitted:
        errors = []
        if not f_name.strip():   errors.append("Full name is required.")
        if not f_email.strip():  errors.append("Email is required.")
        if "@" not in f_email:   errors.append("Valid email is required.")
        if not f_phone.strip():  errors.append("WhatsApp number is required.")

        if errors:
            for err in errors: st.error(f"❌ {err}")
        elif already_registered(f_email.strip()):
            st.warning("⚠️ This email is already registered. If pending, contact support.")
        else:
            base_price = PLANS[f_plan]["price"]
            final_price = round(base_price * (1 - IB_DISCOUNT_PERCENT / 100), 2) if f_ib else base_price
            
            # Save client info as pending
            clients = load_clients()
            clients.append({
                "name": f_name.strip(), "email": f_email.strip().lower(), "phone": f_phone.strip(),
                "country": f_country.strip(), "broker": f_broker.strip(), "account_id": f_acc_id.strip(),
                "plan": f_plan, "amount_due": final_price, "experience": f_exp, "ib_partner": f_ib,
                "status": "pending_payment", "tx_id": "",
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_clients(clients)

            # Move to Step 2
            st.session_state.current_client_email = f_email.strip().lower()
            st.session_state.amount_due = final_price
            st.session_state.step = 'payment'
            st.rerun()

# =====================================================================
# STEP 2: PAYMENT & VERIFICATION
# =====================================================================
elif st.session_state.step == 'payment':
    
    # Check if plan is Trial (Free)
    if st.session_state.amount_due == 0:
        update_client_status(st.session_state.current_client_email, "FREE_TRIAL", status="active")
        st.markdown(f"""
        <div style="background:#ecfdf5; border:2px solid #10b981; border-radius:12px; padding:28px; text-align:center; margin-top:20px;">
            <div style="font-size:36px; margin-bottom:8px;">🎉</div>
            <h2 style="color:#047857; margin:0;">Trial Activated!</h2>
            <p style="color:#065f46; margin-top:10px;">Your 7-day free trial request has been successfully submitted.<br>Our team will send your license key via WhatsApp shortly.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start New Registration"):
            st.session_state.step = 'registration'
            st.rerun()
            
    else:
        st.success("✅ Registration Saved! Please complete your payment below.")
        
        html_success = f"""
        <div style="background:#f0fdf4; border:2px solid #10b981; border-radius:12px; padding:20px; text-align:center; margin-top:10px; margin-bottom:10px;">
            <div style="color:#047857; font-size:16px; font-weight:800; margin-bottom:15px;">STEP 2: COMPLETE PAYMENT</div>
            <div style="color:#6b7280; font-size:12px; text-transform:uppercase; letter-spacing:1px;">Amount to Send</div>
            <div style="color:#111827; font-size:32px; font-weight:900; margin:5px 0;">${st.session_state.amount_due} USDT</div>
            <div style="color:#6b7280; font-size:12px; text-transform:uppercase; letter-spacing:1px; margin-top:16px;">Network</div>
            <div style="color:#0050bb; font-size:16px; font-weight:700;">Solana (SOL)</div>
            <div style="color:#6b7280; font-size:12px; text-transform:uppercase; letter-spacing:1px; margin-top:16px;">Wallet Address (Copy below) 👇</div>
        </div>
        """
        st.markdown(html_success, unsafe_allow_html=True)
        st.code(WALLET_ADDRESS, language="text")

        st.markdown("---")
        st.markdown("### 🔐 Verify Transaction")
        st.markdown("After sending the USDT, paste your **Transaction Hash / Signature** here to instantly verify your payment.")
        
        tx_input = st.text_input("Transaction ID (TxID) / Signature", placeholder="e.g. 5Kx2... (Paste hash here)")
        
        if st.button("🔄 Verify Payment Automatically", use_container_width=True, type="primary"):
            if not tx_input.strip():
                st.error("Please enter a Transaction ID to verify.")
            else:
                with st.spinner("⏳ Checking Solana Blockchain for verification... Please wait"):
                    is_valid, msg = verify_solana_transaction(tx_input, st.session_state.amount_due)
                    
                if is_valid:
                    update_client_status(st.session_state.current_client_email, tx_input, status="paid")
                    st.markdown(f"""
                    <div style="background:#ecfdf5; border:2px solid #10b981; border-radius:12px; padding:20px; text-align:center; margin-top:10px;">
                        <h2 style="color:#047857; margin:0;">🎉 Payment Verified Instantly!</h2>
                        <p style="color:#065f46; margin-top:10px;">Thank you! Your transaction was successful.<br><b>Status: {msg}</b><br><br>Your license key will be sent to your WhatsApp shortly.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Start New Registration"):
                        st.session_state.step = 'registration'
                        st.rerun()
                else:
                    st.error(f"❌ {msg}")
                    st.info("If you just made the payment, it might take a few seconds to appear on the network. Try verifying again in 30 seconds.")

# Footer
st.markdown("""
<div style="text-align:center; margin-top:36px; padding-top:16px; border-top:1px solid #e5e7eb; font-size:11px; color:#6b7280;">
    © 2026 V.Y. TECH · All Rights Reserved
</div>
""", unsafe_allow_html=True)
