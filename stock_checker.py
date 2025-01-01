import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

def check_stock(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
        "Accept-Language": "en-US,en;q=0.9",
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    # Check multiple possible indicators of stock availability
    availability_elements = [
        soup.select_one('#availability span'),
        soup.select_one('#outOfStock'),
        soup.select_one('#add-to-cart-button'),
        soup.select_one('#buyNow'),
    ]

    for element in availability_elements:
        if element:
            if element.get('id') in ['add-to-cart-button', 'buyNow']:
                return True
            elif 'In Stock' in element.text:
                return True
            elif 'Out of Stock' in element.text:
                return False
    return False

# Streamlit app
st.title("Stock Alert")

url = st.text_input("Enter the product URL:")
interval = st.number_input("Enter time interval (in seconds):", min_value=5, value=30, step=5)

if st.button("Check Stock"):
    if url:
        st.write("Checking stock...")
        try:
            while True:
                in_stock = check_stock(url)
                if in_stock:
                    st.success("Item is in stock! 🎉")
                    st.markdown(f"[Buy Now]({url})", unsafe_allow_html=True)
                    break
                else:
                    st.warning("Item is out of stock. Checking again in a few seconds...")
                    time.sleep(interval)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")
