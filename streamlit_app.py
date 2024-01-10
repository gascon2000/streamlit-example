import pandas as pd
import streamlit as st

st.markdown("<h1 style='text-align: center;'>PandaQ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Josep Gascon</p>", unsafe_allow_html=True)
st.write("")

st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

selected = st.text_input("", "Select * from countries;")
button_clicked = st.button("Submit")


# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("final.csv")
    return df
data = load_data().copy()


nazev_column = st.column_config.TextColumn(label="Název společnti")
market_cap_column = st.column_config.TextColumn(label="Tržní kapitalizace 💬",help="📍**v mld. USD**")
price_column = st.column_config.TextColumn(label="Cena za 1 akcii 💬", help="📍**Uzavírací cena za předchozí den (v USD)**")

# Adjust the index to start from 1 and display only the first 25 companies
data.reset_index(drop=True, inplace=True)
data = data.head(25)
data.index = data.index + 1
data = data[['Name', 'Market Cap', 'Price']]

# Display the dataframe
st.dataframe(data, height=913, column_config={"Name":nazev_column,'Market Cap':market_cap_column,'Price':price_column})




