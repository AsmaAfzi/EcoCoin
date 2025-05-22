import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000"

st.title("EcoCoin Wallet Dashboard")

menu = st.sidebar.radio("Menu", ["Wallet Balance", "Send EcoCoins", "View Blockchain"])

if menu == "Wallet Balance":
    wallet = st.text_input("Enter your wallet ID")
    if st.button("Check Balance"):
        r = requests.get(f"{BACKEND_URL}/get_balance/{wallet}")
        st.json(r.json())

elif menu == "Send EcoCoins":
    sender = st.text_input("Sender Wallet ID")
    receiver = st.text_input("Receiver Wallet ID")
    amount = st.number_input("Amount", min_value=1)
    if st.button("Send"):
        r = requests.post(f"{BACKEND_URL}/add_transaction", json={
            "sender": sender, "receiver": receiver, "amount": amount
        })
        st.json(r.json())

elif menu == "View Blockchain":
    r = requests.get(f"{BACKEND_URL}/get_chain")
    st.json(r.json())
