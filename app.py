import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Excel Address Geocoder", layout="centered")
st.title("📍 Excel Address Geocoder")

# Ask for API Key
api_key = st.text_input("🔑 Enter your Google Maps API Key:", type="password")

def get_coordinates(address, key):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': key}
    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        location = response['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

uploaded_file = st.file_uploader("Upload an Excel file", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Preview of uploaded file:")
    st.dataframe(df.head())

    column_options = df.columns.tolist()
    address_column = st.selectbox("Select the column containing addresses:", column_options)

    if st.button("🔍 Fetch Coordinates"):
        if not api_key:
            st.warning("⚠️ Please enter your API key before proceeding.")
        else:
            with st.spinner("Fetching coordinates..."):
                df['Latitude'], df['Longitude'] = zip(*df[address_column].map(lambda x: get_coordinates(x, api_key)))

            st.success("✅ Coordinates added successfully!")
            st.dataframe(df)

            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            st.download_button(
                label="⬇ Download Result Excel",
                data=buffer.getvalue(),
                file_name="geocoded_addresses.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
