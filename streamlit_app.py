import pandas as pd
import streamlit as st
from PIL import Image
import base64
import io
import os

# Vykreslení tabulky s logy
st.markdown("<h1 style='text-align: center;'>Žebříček největších společností světa</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Podle tržní kapitalizace v miliardách dolarů </p>", unsafe_allow_html=True)
st.write("")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

icon("search")
selected = st.text_input("", "Search...")
button_clicked = st.button("OK")



# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("final.csv")
    return df

data = load_data().copy()

# Convert image to Base64
def image_to_base64(img_path, output_size=(64, 64)):
    # Check if the image path exists
    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            img = img.resize(output_size)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
    return ""

# If 'Logo' column doesn't exist, create one with path to the logos
if 'Logo' not in data.columns:
    output_dir = 'downloaded_logos'
    data['Logo'] = data['Name'].apply(lambda name: os.path.join(output_dir, f'{name}.png'))

# Convert image paths to Base64
data["Logo"] = data["Logo"].apply(image_to_base64)

nazev_column = st.column_config.TextColumn(label="Název společnosti")
market_cap_column = st.column_config.TextColumn(label="Tržní kapitalizace 💬",help="📍**v mld. USD**")
price_column = st.column_config.TextColumn(label="Cena za 1 akcii 💬", help="📍**Uzavírací cena za předchozí den (v USD)**")

# Adjust the index to start from 1 and display only the first 25 companies
data.reset_index(drop=True, inplace=True)
data = data.head(25)
data.index = data.index + 1

data = data[['Name', 'Market Cap', 'Price']]


# Display the dataframe
st.dataframe(data, height=913, column_config={"Name":nazev_column,'Market Cap':market_cap_column,'Price':price_column})

import datetime

# Získání aktuálního data
dnesni_datum = datetime.date.today().strftime("%d.%m.%Y")  # Formátování data na formát DD.MM.YYYY

st.markdown(f'<span style="font-size: 14px">**Zdroj:** companiesmarketcap.com | **Data:** k {dnesni_datum} | **Autor:** lig </span>', unsafe_allow_html=True)
