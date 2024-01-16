import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import seaborn as sns

# Fungsi untuk visualisasi sebaran sentimen terhadap setiap aspek
def plot_sentiment_by_aspect(data):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='kategori aspek', hue='label', data=data)
    plt.title('Sentiment Distribution by Aspect')
    plt.xlabel('Aspect')
    plt.ylabel('Number of Reviews')
    return plt

# Fungsi untuk menghitung informasi tambahan
def calculate_additional_info(data):
    total_reviews = len(data)
    most_common_aspect = data['kategori aspek'].value_counts().idxmax()
    most_common_aspect_count = data['kategori aspek'].value_counts().max()
    most_common_sentiment = data['label'].value_counts().idxmax()
    most_common_sentiment_count = data['label'].value_counts().max()
    return total_reviews, most_common_aspect, most_common_aspect_count, most_common_sentiment, most_common_sentiment_count

# Fungsi untuk membuat wordcloud
def create_wordcloud(data, aspect, sentiment):
    text = " ".join(review for review in data[data["kategori aspek"] == aspect][data["label"] == sentiment]["ulasan"])
    wordcloud = WordCloud(background_color="white").generate(text)
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
    st.set_page_config(page_title="Dashboard Sentimen Ulasan Pengunjung Pariwisata Banyuwangi")
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
                    st.write(data)
                    st.session_state['data'] = data
                    st.success("File Uploaded Successfully")
                except Exception as e:
                    st.error(f"Error reading file: {e}")

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
                    st.pyplot(plot_pie_chart(data))

                with col2:
                    st.subheader("Total Reviews")
                    st.write(total_reviews)
                    st.text("Most Common Aspect:")
                    st.text(f"{most_common_aspect} ({most_common_aspect_count})")
                    st.text("Most Common Sentiment:")
                    st.text(f"{most_common_sentiment} ({most_common_sentiment_count})")

                with col3:
                    st.subheader("Aspect Distribution")
                    st.pyplot(plot_histogram(data))

                # Box sebaran sentimen terhadap setiap aspek
                st.subheader("Sentiment Distribution by Aspect")
                sentiment_by_aspect_plot = plot_sentiment_by_aspect(data)
                st.pyplot(sentiment_by_aspect_plot)


            else:
                st.warning("No data available. Please upload a file.")

            # Wordcloud
        elif menu == "Wordcloud":
            st.header("Wordcloud")
            sentiment = st.sidebar.selectbox("Select Sentiment", ["Positive", "Negative", "Neutral"])

            if 'data' in st.session_state:
                data = st.session_state['data']
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.subheader("Attraction")
                    wc_attraction = create_wordcloud(data, "atraksi", sentiment.lower())
                    plt.imshow(wc_attraction, interpolation='bilinear')
                    plt.axis("off")
                    st.pyplot()

                with col2:
                    st.subheader("Amenities")
                    wc_amenities = create_wordcloud(data, "amenitas", sentiment.lower())
                    plt.imshow(wc_amenities, interpolation='bilinear')
                    plt.axis("off")
                    st.pyplot()

                with col3:
                    st.subheader("Accessibility")
                    wc_accessibility = create_wordcloud(data, "aksebilitas", sentiment.lower())
                    plt.imshow(wc_accessibility, interpolation='bilinear')
                    plt.axis("off")
                    st.pyplot()

            else:
                st.warning("No data available. Please upload a file.")

# Jalankan aplikasi
if __name__ == "__main__":
    main()
