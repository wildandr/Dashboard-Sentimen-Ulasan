import streamlit as st
import pandas as pd
import os
from PIL import Image
import csv
import hashlib
from textblob import TextBlob
import pandas as pd
import os

# Setup awal Streamlit dan fungsi utility
st.set_page_config(page_title="Dashboard Sentimen Ulasan Pengunjung Pariwisata Banyuwangi", layout="wide")

def save_user_data(username, password, remember_me):
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Hash password sebelum menyimpan
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        writer.writerow([username, hashed_password, remember_me])

def display_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("Dashboard Sentimen Ulasan Pengunjung Pariwisata Banyuwangi")
    with col2:
        if os.path.exists('Logo.png'):
            logo = Image.open('Logo.png')
            st.image(logo, width=100)

# Halaman Login
def login_page():
    display_header()
    st.subheader("Selamat Datang")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    remember_me = st.checkbox("Remember Me")
    if st.button("Login"):
        save_user_data(username, password, remember_me)
        st.session_state['logged_in'] = True
        st.success("Login Berhasil!")

# Halaman Upload File
def upload_page():
    display_header()
    st.subheader("Upload Data")
    uploaded_file = st.file_uploader("Pilih Data", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        # Simpan file yang diunggah ke tempat penyimpanan sementara
        file_path = os.path.join("temp_uploaded", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File berhasil diunggah.")
    if st.button("Clear Data"):
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success("Data berhasil dihapus.")



# Fungsi untuk melakukan analisis sentimen
def analyze_sentiment(text):
    testimonial = TextBlob(text)
    polarity = testimonial.sentiment.polarity
    if polarity > 0:
        return "Positif"
    elif polarity == 0:
        return "Netral"
    else:
        return "Negatif"

# Fungsi untuk menyimpan file yang diunggah
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_path = os.path.join("uploaded_files", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

# Fungsi untuk memproses data Excel dan melakukan analisis
def process_data(file_path):
    try:
        data = pd.read_excel(file_path)
        # Tambahkan lebih banyak preprocessing di sini jika diperlukan
        data['predicted_sentiment'] = data['ulasan'].apply(analyze_sentiment)
        return data
    except Exception as e:
        st.error(f"Error saat memproses data: {e}")
        return None

# Fungsi Halaman Awal
def home_page():
    display_header()
    if os.path.exists('Logo.png'):
        logo = Image.open('Logo.png')
        st.image(logo, width=200)
    if st.button("Input Data Set"):
        uploaded_file = st.file_uploader("Pilih Data", type=['xlsx'])
        if uploaded_file is not None:
            file_path = save_uploaded_file(uploaded_file)
            if file_path:
                data = process_data(file_path)
                if data is not None:
                    st.write(data)
    if st.button("Hasil Analisis"):
        # Tambahkan logika khusus untuk menampilkan hasil analisis di sini
        st.info("Tampilkan Hasil Analisis (implementasi logika analisis)")

# Sisa fungsi yang diperlukan (seperti display_header, main, dll) tetap sama


# Halaman Analisis
def analysis_page():
    display_header()
    if st.button("Ke Halaman Awal"):
        home_page()
    if st.button("Ke Halaman Wordcloud"):
        wordcloud_page()
    st.info("Visualisasi data di sini (implementasi visualisasi)")

# Halaman Wordcloud
def wordcloud_page():
    display_header()
    st.subheader("Wordcloud")
    sentiment = st.selectbox("Pilih Sentimen", ["Positif", "Negatif", "Netral"])
    st.info(f"Wordcloud untuk sentimen {sentiment} (implementasi wordcloud)")

# Main
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.sidebar.title("Navigasi")
        choice = st.sidebar.radio("Pilih Halaman:", ["Home", "Upload", "Analisis", "Wordcloud"])

        if choice == "Home":
            home_page()
        elif choice == "Upload":
            upload_page()
        elif choice == "Analisis":
            analysis_page()
        elif choice == "Wordcloud":
            wordcloud_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
