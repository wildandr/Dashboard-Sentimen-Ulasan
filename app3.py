import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import seaborn as sns
import nltk
import re
import string
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Load your slang words DataFrame
df_slang = pd.read_csv('/workspaces/Dashboard-Sentimen-Ulasan/colloquial-indonesian-lexicon.csv')

def preprocess_reviews(data):
    # Remove numbers
    data['cleaned_ulasan'] = data['ulasan'].str.replace(r'[\d+]', ' ', regex=True)

    # Remove punctuation
    data['cleaned_ulasan'] = data['cleaned_ulasan'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))

    # Remove extra whitespaces
    data['cleaned_ulasan'] = data['cleaned_ulasan'].str.strip().replace(r'\s\s+', ' ', regex=True)

    # Convert to lowercase and remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002500-\U00002BEF"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    data['cleaned_ulasan'] = data['cleaned_ulasan'].str.lower().replace(emoji_pattern, ' ', regex=True)

    # Replace slang words
    def replace_slang(phrase):
        return ' '.join([df_slang.loc[df_slang['slang'] == word, 'formal'].iloc[0] if word in df_slang['slang'].values else word for word in phrase.split()])

    data['cleaned_ulasan'] = data['cleaned_ulasan'].apply(replace_slang)

    # Tokenization
    nltk.download('punkt')
    data['cleaned_ulasan'] = data['cleaned_ulasan'].apply(word_tokenize)

    # Remove stopwords
    nltk.download('stopwords')
    indonesian_stopwords = set(stopwords.words('indonesian'))
    data['cleaned_ulasan'] = data['cleaned_ulasan'].apply(lambda x: [word for word in x if word not in indonesian_stopwords])

    # Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    data['cleaned_ulasan'] = data['cleaned_ulasan'].apply(lambda x: [stemmer.stem(word) for word in x])

    # Rejoin words
    data['cleaned_ulasan'] = data['cleaned_ulasan'].apply(lambda x: ' '.join(x))

    return data

# Fungsi untuk visualisasi sebaran sentimen terhadap setiap aspek
def plot_sentiment_by_aspect(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='kategori aspek', hue='label', data=data, ax=ax)
    ax.set_title('Sentiment Distribution by Aspect')
    ax.set_xlabel('Aspect')
    ax.set_ylabel('Number of Reviews')
    return fig

# Fungsi untuk menghitung informasi tambahan
def calculate_additional_info(data):
    total_reviews = len(data)
    most_common_aspect = data['kategori aspek'].value_counts().idxmax()
    most_common_aspect_count = data['kategori aspek'].value_counts().max()
    most_common_sentiment = data['label'].value_counts().idxmax()
    most_common_sentiment_count = data['label'].value_counts().max()
    return total_reviews, most_common_aspect, most_common_aspect_count, most_common_sentiment, most_common_sentiment_count

def create_wordcloud(data, aspect, sentiment):
    # Pastikan DataFrame difilter dengan benar
    filtered_data = data[(data["kategori aspek"].str.lower() == aspect.lower()) & 
                         (data["label"].str.lower() == sentiment.lower())]
    
    # Gabungkan semua ulasan menjadi satu string
    text = " ".join(review.strip() for review in filtered_data["ulasan"])

    # Jika tidak ada teks, buat wordcloud kosong
    wordcloud = WordCloud(background_color="white", width=800, height=400)
    if text:
        wordcloud.generate(text)
    else:
        # Buat wordcloud kosong dengan teks default seperti "Tidak ada data"
        wordcloud.generate("Tidak ada data")
    
    return wordcloud

# Fungsi untuk menampilkan pie chart
def plot_pie_chart(data):
    sentiment_counts = data['label'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
    return fig

# Fungsi untuk menampilkan histogram
def plot_histogram(data):
    fig, ax = plt.subplots()
    data['kategori aspek'].value_counts().plot(ax=ax, kind='bar')
    return fig

# Fungsi untuk login
def login_user(username, password):
    if username == "admin" and password == "password":  # Contoh sederhana
        return True
    return False

# Fungsi utama Streamlit
def main():
    st.set_page_config(page_title="Dashboard Sentimen Ulasan Pengunjung Pariwisata Banyuwangi", layout='wide')
    st.image("Logo.png", width=100)
    st.title("Dashboard Sentimen Ulasan Pengunjung Pariwisata Banyuwangi")

    # Login
    if 'login_status' not in st.session_state or not st.session_state['login_status']:
        with st.form("Login Form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            remember_me = st.checkbox("Remember me")
            submitted = st.form_submit_button("Login")
            if submitted:
                if login_user(username, password):
                    st.session_state['login_status'] = True
                    if remember_me:
                        st.session_state['username'] = username
                else:
                    st.error("Incorrect username/password")

    if 'login_status' in st.session_state and st.session_state['login_status']:
        menu = st.sidebar.radio("Navigation", ["Upload File", "Analysis", "Wordcloud"])

        # Upload File
        if menu == "Upload File":
            st.header("Upload File")
            uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
            if uploaded_file is not None:
                try:
                    # Membaca file Excel
                    data = pd.read_excel(uploaded_file)

                    # Apply preprocessing
                    preprocessed_data = preprocess_reviews(data)

                    st.write(preprocessed_data)  # Display the preprocessed data
                    st.session_state['data'] = preprocessed_data  # Store the preprocessed data in session
                    st.success("File Uploaded and Preprocessed Successfully")
                except Exception as e:
                    st.error(f"Error reading or preprocessing file: {e}")

        # Analysis
        elif menu == "Analysis":
            st.header("Analysis")
            if 'data' in st.session_state:
                data = st.session_state['data']

                # Menghitung informasi tambahan
                total_reviews, most_common_aspect, most_common_aspect_count, most_common_sentiment, most_common_sentiment_count = calculate_additional_info(data)

                # Layout kolom untuk visualisasi dan info tambahan
                col1, col2 , col3 = st.columns(3)

                with col1:
                    st.subheader("Sentiment Distribution")
                    fig_pie_chart = plot_pie_chart(data)
                    st.pyplot(fig_pie_chart)

                with col2:
                    st.subheader("Total Reviews")
                    st.write(total_reviews)
                    st.text("Most Common Aspect:")
                    st.text(f"{most_common_aspect} ({most_common_aspect_count})")
                    st.text("Most Common Sentiment:")
                    st.text(f"{most_common_sentiment} ({most_common_sentiment_count})")

                with col3:
                    st.subheader("Aspect Distribution")
                    fig_histogram = plot_histogram(data)
                    st.pyplot(fig_histogram)

                st.subheader("Sentiment Distribution by Aspect")
                fig_sentiment_by_aspect = plot_sentiment_by_aspect(data)
                st.pyplot(fig_sentiment_by_aspect)

            else:
                st.warning("No data available. Please upload a file.")

        # Opsi menu "Wordcloud"
        elif menu == "Wordcloud":
            st.header("Wordcloud")
            sentiment = st.sidebar.selectbox("Pilih Sentimen", ["Positif", "Negatif", "Netral"])

            if 'data' in st.session_state and not st.session_state['data'].empty:
                data = st.session_state['data']
                col1, col2, col3 = st.columns(3)

                aspects = ['atraksi', 'amenitas', 'aksesibilitas']
                for i, aspect in enumerate(aspects):
                    with (col1, col2, col3)[i]:
                        st.subheader(f"{aspect.capitalize()}")
                        wordcloud = create_wordcloud(data, aspect, sentiment.lower())
                        if wordcloud:
                            fig, ax = plt.subplots()
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis("off")
                            st.pyplot(fig)  # Sekarang meneruskan objek fig ke st.pyplot()
                        else:
                            st.error(f"Tidak ada cukup teks untuk aspek '{aspect}' dengan sentimen '{sentiment}'.")

# Jalankan aplikasi
if __name__ == "__main__":
    main()
