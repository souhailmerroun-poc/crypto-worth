import streamlit as st
import requests
import pandas as pd

# Function to fetch current cryptocurrency price
def get_current_crypto_price(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    try:
        return data[crypto]['usd']
    except KeyError:
        st.error(f"Error fetching price for {crypto.upper()}. Please try again later.")
        return None

# Function to calculate worth at different price scenarios
def calculate_worth(btc_amount, current_price, percentage):
    scenarios = []
    # Calculating scenarios based on percentage change in price
    for i in range(-5, 6):  # 5 scenarios below and above the current price
        adjusted_price = current_price * ((100 + percentage * i) / 100)
        worth = btc_amount * adjusted_price
        price_change_percent = percentage * i
        scenarios.append({
            'Crypto Price': f"${int(adjusted_price):,}",  # Formatted with comma
            'Change (%)': f"{price_change_percent:.2f}",
            'Worth (USD)': f"${int(worth):,}"  # Formatted with comma
        })

    df = pd.DataFrame(scenarios)

    # Highlight the current crypto price row
    def highlight_current_price(row):
        if row['Crypto Price'] == f"${int(current_price):,}":
            return ['background-color: yellow']*3
        else:
            return ['']*3

    return df.style.apply(highlight_current_price, axis=1)

# Streamlit app
def main():
    st.title('Cryptocurrency Investment Calculator')

    # User choice of cryptocurrency
    crypto_choice = st.selectbox('Choose the cryptocurrency:', ['bitcoin', 'ethereum'])

    # User input for amount of cryptocurrency, with default value
    default_crypto_amount = 0.3147692
    crypto_amount = st.number_input(f'Enter the amount of {crypto_choice} you own:', min_value=0.0, value=default_crypto_amount, format='%f')

    # User selectable percentage increments
    percentage_options = {'3%': 3, '5% (default)': 5, '10%': 10, '20%': 20, 'Custom': 0}
    selected_percentage = st.selectbox('Select the percentage increment:', list(percentage_options.keys()))

    # Custom percentage input
    if selected_percentage == 'Custom':
        custom_percentage = st.number_input('Enter custom percentage:', min_value=0.01, format='%f')
        percentage = custom_percentage
    else:
        percentage = percentage_options[selected_percentage]

    # Fetch and display current cryptocurrency price
    current_price = get_current_crypto_price(crypto_choice.lower())
    st.write(f'Current {crypto_choice} Price: ${int(current_price):,}')  # Formatted with comma

    # Calculate and display worth for different scenarios
    df_styled = calculate_worth(crypto_amount, current_price, percentage)
    st.dataframe(df_styled)

if __name__ == "__main__":
    main()
