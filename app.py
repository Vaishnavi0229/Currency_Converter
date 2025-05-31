import streamlit as st
import requests

st.set_page_config(page_title="Currency Converter", page_icon="💱")
st.title("Currency Converter")
st.write("Convert currency in real-time using live exchange rates.")

@st.cache_data
def get_currency_data():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

data = get_currency_data()

if data is None or "rates" not in data:
    st.error("Failed to load currency data.")
    st.stop()

currency_list = list(data["rates"].keys())

from_currency = st.selectbox("From Currency", currency_list, index=currency_list.index("USD"))
to_currency = st.selectbox("To Currency", currency_list, index=currency_list.index("EUR"))
amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")

if st.button("Convert"):
    try:
        rate_from = data["rates"][from_currency]
        rate_to = data["rates"][to_currency]
        result = (rate_to / rate_from) * amount
        st.success(f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}")
    except Exception as e:
        st.error(f"Conversion failed: {e}")