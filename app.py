import streamlit as st
import pandas as pd
import os
from PIL import Image
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Konfigurasi Page
st.set_page_config(page_title="Dashboard Sentimen Ulasan Pengunjung Pariwisata Banyuwangi", layout="wide")

# Load Logo
logo_path = "Logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
else:
    logo = None  # Atau gambar default jika logo tidak ditemukan

# Fungsi untuk menampilkan header
def display_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("Dashboard Sentimen Ulasan Pengunjung Pariwisata Banyuwangi")
    with col2:
        if logo:
            st.image(logo, width=100)

# Fungsi untuk menyimpan data pengguna
def save_user_data(username, password, remember_me):
    # Lokasi file CSV
    csv_file = 'users.csv'
    new_data = [username, password, 'Yes' if remember_me else 'No']

    # Cek jika file sudah ada
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Tulis header jika file baru
            writer.writerow(['Username', 'Password', 'Remember Me'])
            writer.writerow(new_data)
    else:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_data)

# Fungsi Halaman Login
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

# Direktori untuk menyimpan file yang diunggah
upload_directory = "uploaded_files"
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)

# Fungsi untuk menyimpan file yang diunggah
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_path = os.path.join(upload_directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

# Fungsi untuk menampilkan data dari file yang diunggah
def display_uploaded_data(file_path):
    if file_path:
        file_extension = os.path.splitext(file_path)[1]
        if file_extension.lower() == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        st.dataframe(df)

# Fungsi Halaman Upload
def upload_page():
    display_header()
    st.subheader("Upload Data")
    uploaded_file = st.file_uploader("Pilih Data", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        if st.button("Clear Data"):
            if os.path.exists(file_path):
                os.remove(file_path)
                st.session_state.pop('uploaded_file_path', None)
                st.success("Data berhasil dihapus.")
        if st.button("Upload Data"):
            st.session_state['uploaded_file_path'] = file_path
            st.success("Data berhasil diunggah.")


# Fungsi Halaman Awal
def home_page():
    display_header()
    if logo:
        st.image(logo, width=200)

    # Tombol untuk memulai proses input data set
    if st.button("Input Data Set"):
        # Update session state to navigate to upload page
        st.session_state['current_page'] = 'upload_page'
        # Rerun the script to reflect the change
        st.experimental_rerun()

    # Tombol untuk melihat hasil analisis
    if st.button("Hasil Analisis"):
        st.session_state['current_page'] = 'analysis'
        st.experimental_rerun()

# Fungsi untuk membuat pie chart
def create_pie_chart(data, title):
    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title(title)
    return fig

# Fungsi untuk membuat histogram
def create_histogram(data, title):
    fig, ax = plt.subplots()
    sns.barplot(x=data.index, y=data.values, ax=ax)
    plt.title(title)
    plt.xticks(rotation=45)
    return fig

# Fungsi Halaman Analisis
def analysis_page(df):
    display_header()

    # Tombol navigasi
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Ke Halaman Awal"):
            st.session_state['current_page'] = 'home'
            st.rerun()
    with col2:
        if st.button("Ke Halaman Wordcloud"):
            st.session_state['current_page'] = 'wordcloud'
            st.rerun()
    with col3:
        if st.button("Ke Halaman Overview"):
            # Navigasi ke halaman overview
            pass
    with col4:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Menganalisis data
    sentiment_counts = df['label'].value_counts()
    aspect_counts = df['kategori aspek'].value_counts()

    # Visualisasi
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Visualisasi Sentimen")
        fig1 = create_pie_chart(sentiment_counts, "Sebaran Sentimen")
        st.pyplot(fig1)
    with col2:
        st.subheader("Informasi Tambahan")
        st.write(f"Total Ulasan: {len(df)}")
        most_common_aspect = aspect_counts.idxmax()
        most_common_sentiment = sentiment_counts.idxmax()
        st.write(f"Aspek Terbanyak: {most_common_aspect} ({aspect_counts[most_common_aspect]})")
        st.write(f"Sentimen Terbanyak: {most_common_sentiment} ({sentiment_counts[most_common_sentiment]})")

    st.subheader("Visualisasi Aspek")
    fig2 = create_histogram(aspect_counts, "Sebaran Jumlah Ulasan Berdasarkan Aspek")
    st.pyplot(fig2)



import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Fungsi untuk menampilkan header
def display_header():
    st.header("Dashboard Sentimen Ulasan Pengunjung Pariwisata Banyuwangi")
    # Tambahkan kode untuk menampilkan logo jika ada

# Fungsi untuk membuat wordcloud
def create_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

# Fungsi Halaman Wordcloud
def wordcloud_page(df):
    display_header()
    st.subheader("Wordcloud")

    # Pilihan sentimen
    choice = st.selectbox("Pilih Sentimen", ["Positif", "Negatif", "Netral"])
    
    # Filter data berdasarkan sentimen yang dipilih
    filtered_df = df[df['label'] == choice.lower()]

    # Membuat wordcloud untuk setiap kategori aspek
    aspect_categories = filtered_df['kategori aspek'].unique()
    col1, col2, col3 = st.columns(3)

    with col1:
        if 'atraksi' in aspect_categories:
            st.subheader("Atraksi")
            atraksi_text = ' '.join(filtered_df[filtered_df['kategori aspek'] == 'atraksi']['ulasan'])
            fig = create_wordcloud(atraksi_text)
            st.pyplot(fig)

    with col2:
        if 'amenitas' in aspect_categories:
            st.subheader("Amenitas")
            amenitas_text = ' '.join(filtered_df[filtered_df['kategori aspek'] == 'amenitas']['ulasan'])
            fig = create_wordcloud(amenitas_text)
            st.pyplot(fig)

    with col3:
        if 'aksesibilitas' in aspect_categories:
            st.subheader("Aksesibilitas")
            aksesibilitas_text = ' '.join(filtered_df[filtered_df['kategori aspek'] == 'aksesibilitas']['ulasan'])
            fig = create_wordcloud(aksesibilitas_text)
            st.pyplot(fig)


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        page = st.sidebar.selectbox("Pilih Halaman", ["Home", "Upload File", "Analisis", "Wordcloud"])

        if page == "Home":
            home_page()
        elif page == "Upload File":
            upload_page()
        elif page == "Analisis" or page == "Wordcloud":
            if 'uploaded_file_path' in st.session_state and os.path.exists(st.session_state['uploaded_file_path']):
                file_path = st.session_state['uploaded_file_path']
                # Load dataframe
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                # Render respective page
                if page == "Analisis":
                    analysis_page(df)
                elif page == "Wordcloud":
                    wordcloud_page(df)
            else:
                st.error("Please upload a file in the 'Upload File' section first.")
    else:
        login_page()

if __name__ == "__main__":
    main()


