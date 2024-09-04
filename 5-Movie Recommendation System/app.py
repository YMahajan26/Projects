import streamlit as st
import pickle
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
from tenacity import retry, wait_fixed, stop_after_attempt

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=27287136ab9f13d89fa18323040dc2af&language=en-US"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

    recommended_movies_posters = []
    recommended_movies = []
    for i in movies_list[1:7]:
        movie_id = movies.iloc[i[0]].id
        try:
            poster = fetch_poster(movie_id)
            recommended_movies_posters.append(poster)
            recommended_movies.append(movies.iloc[i[0]].title)
        except Exception as e:
            st.error(f"An error occurred while fetching poster for {movies.iloc[i[0]].title}: {e}")
            recommended_movies_posters.append(None)
            recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

st.title("Movie Recommendation System")

selected_movie_option = st.selectbox("Select a movie you like", movies_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_option)
    
    for i in range(0, 6, 3):
        cols = st.columns(3)
        for idx, col in enumerate(cols):
            if i + idx < len(names):
                if posters[i + idx]:
                    col.image(posters[i + idx])
                col.text(names[i + idx])
