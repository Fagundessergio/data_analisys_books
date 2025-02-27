import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
import time

st.set_page_config(page_title="Avaliações", page_icon=":books:", layout="wide")
  
st.title("📝 Avaliações de Livros")

with st.spinner("Carregando os dados..."):
    df_reviews = pd.read_csv(r"D:\Programação\Desenvolvimento\Estudos Backend\Python\portifolio_analise_dados\data_analysis_books\dataset\customer reviews.csv")
    df_top100_books = pd.read_csv(r"D:\Programação\Desenvolvimento\Estudos Backend\Python\portifolio_analise_dados\data_analysis_books\dataset\Top-100 Trending Books.csv")

books = df_top100_books["book title"].unique()
book = st.sidebar.selectbox("Selecione um livro", books)

df_books = df_top100_books[df_top100_books["book title"] == book]
df_reviews_f = df_reviews[df_reviews["book name"] == book]

book_title = df_books["book title"].iloc[0]
book_genre = df_books["genre"].iloc[0]
book_price = f"R${df_books['book price'].iloc[0]:.2f}"
book_rating = df_books["rating"].iloc[0]
book_year = df_books["year of publication"].iloc[0]

st.title(book_title)
st.subheader(book_genre)
st.write(book_genre)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div style="background-color: #f0f0f5; padding: 10px; border-radius: 30px; text-align: center;">
            <h3 style="color: #2a9d8f;">Preço do Livro</h3>
            <p style="font-size: 20px; font-weight: bold; color: #264653;">{book_price}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"""
        <div style="background-color: #f0f0f5; padding: 10px; border-radius: 30px; text-align: center;">
            <h3 style="color: #2a9d8f;">Avaliação do Livro</h3>
            <p style="font-size: 20px; font-weight: bold; color: #264653;">{book_rating}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"""
        <div style="background-color: #f0f0f5; padding: 10px; border-radius: 30px; text-align: center;">
            <h3 style="color: #2a9d8f;">Ano de Publicação</h3>
            <p style="font-size: 20px; font-weight: bold; color: #264653;">{book_year}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
st.divider()

if df_reviews_f.empty:
    # Animação de lágrimas caindo
    st.markdown("""
    <style>
        .no-reviews {
            font-size: 24px;
            font-weight: bold;
            color: #e63946;
            text-align: center;
            position: relative;
            padding: 50px;
        }
        .tear {
            position: absolute;
            animation: tear 2s infinite;
        }
        .tear:nth-child(1) {
            left: 30%;
            top: 20%;
            animation-delay: 0.5s;
        }
        .tear:nth-child(2) {
            left: 50%;
            top: 30%;
            animation-delay: 1s;
        }
        .tear:nth-child(3) {
            left: 70%;
            top: 40%;
            animation-delay: 1.5s;
        }
        @keyframes tear {
            0% { transform: translateY(0); opacity: 1; }
            100% { transform: translateY(30px); opacity: 0; }
        }
    </style>
    <div class="no-reviews">
        Não há avaliações disponíveis para este livro.
        <div class="tear">😭</div>
        <div class="tear">😭</div>
        <div class="tear">😭</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for row in df_reviews_f.values:
        review = row[4] if pd.notna(row[4]) else "Sem revisão"
        
        st.markdown(f"**{row[2]}**")  # Nome do revisor
        st.write(f"**Avaliação:** {row[5]}")  # Avaliação do livro
        st.write(f"Revisão: {review}")  # Texto da revisão
        st.divider()
