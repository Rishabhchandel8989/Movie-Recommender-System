import pandas as pd
import streamlit as st
import pickle
import requests

# Always on cloud flare vpn

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2da46720fd3392741bc07f911a00be9d&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']


st.set_page_config(page_title="Movie Recommender 🎬", page_icon="🎥", layout="wide")

st.markdown("""
    <style>
    /* Background image */
    .main {
        # background: url('https://editor.analyticsvidhya.com/uploads/76889recommender-system-for-movie-recommendation.jpg') no-repeat center center fixed;
        background: url('F:\Movie_recommender_app\76889recommender-system-for-movie-recommendation.jpg') no-repeat center center fixed;
        background-size: cover;
    }
    
    /* Dark overlay */
    .overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: -1;
    }

    h1 {
        text-align: center;
        color: #FFD700; /* Premium gold */
        font-size: 3rem !important;

        font-weight: bold;
        text-shadow: 2px 2px 10px black;
    }

    .movie-card {
        padding: 10px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.1); /* Glassmorphism */
        backdrop-filter: blur(10px);
        text-align: center;
        transition: 0.3s;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .movie-card:hover {
        transform: scale(1.05);
        background: rgba(255, 215, 0, 0.15); /* Gold hover */
    }
    .movie-title {
        font-size: 1.1rem;
        margin-top: 10px;
        color: white;
        font-weight: bold;
    }
    </style>
    <div class="overlay"></div>
""", unsafe_allow_html=True)

similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movie = pd.DataFrame(movie_dict)

def recommend(movies_title):
    movies_index = movie[movie['title'] == movies_title].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movie = []
    recommended_movies_posters = []
    for i in movies_list:
        movies_id = movie.iloc[i[0]].movie_id
        recommend_movie.append(movie.iloc[i[0]].title)  
        recommended_movies_posters.append(fetch_poster(movies_id))
    return recommend_movie, recommended_movies_posters

st.title("🍿 Movie Recommender System 🎥")
selected_movie_name = st.selectbox('🎯 Select a movie', movie['title'].values)

if st.button('🚀 Recommend'):
    names, posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[idx]}" width="100%" style="border-radius:10px;">
                    <div class="movie-title">{names[idx]}</div>
                </div>
            """, unsafe_allow_html=True)







