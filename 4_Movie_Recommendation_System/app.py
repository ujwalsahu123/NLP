import pickle
import streamlit as st
import requests

st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
    }
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 28%),
            radial-gradient(circle at top right, rgba(245,158,11,0.16), transparent 22%),
            linear-gradient(180deg, #0f172a 0%, #111827 16%, #f3f4f6 16%, #f3f4f6 100%);
        background-attachment: fixed;
    }
    .main .block-container {
        max-width: 1200px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }
    .page-shell {
        padding: 0.25rem 0 0.75rem 0;
    }
    .hero {
        background: linear-gradient(135deg, rgba(15,23,42,0.98), rgba(30,41,59,0.94));
        color: white;
        border-radius: 26px;
        padding: 2rem 2rem;
        box-shadow: 0 24px 60px rgba(15,23,42,0.22);
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        margin: 0;
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.05;
    }
    .hero p {
        margin: 0.7rem 0 0 0;
        color: rgba(255,255,255,0.78);
        font-size: 1.02rem;
        max-width: 58ch;
    }
    .kicker {
        display: inline-block;
        margin-bottom: 0.8rem;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.09);
        color: rgba(255,255,255,0.82);
        font-size: 0.82rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .panel {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(10px);
        border-radius: 22px;
        padding: 1.2rem 1.25rem;
        box-shadow: 0 12px 32px rgba(15,23,42,0.08);
        border: 1px solid rgba(148,163,184,0.18);
        height: 100%;
    }
    .panel h3 {
        margin: 0 0 0.45rem 0;
        font-size: 1.05rem;
        color: #111827;
    }
    .panel p {
        margin: 0;
        color: #475569;
        line-height: 1.6;
    }
    .panel-spacer {
        height: 0.9rem;
    }
    .stSelectbox label {
        font-weight: 700;
        color: #111827;
    }
    div[data-baseweb="select"] > div {
        min-height: 3.6rem;
        border-radius: 16px;
        border-color: rgba(148,163,184,0.45);
        box-shadow: 0 8px 18px rgba(15,23,42,0.05);
    }
    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        background: linear-gradient(135deg, #2563eb, #0f172a);
        color: white;
        font-weight: 700;
        box-shadow: 0 14px 24px rgba(37,99,235,0.22);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 16px 28px rgba(37,99,235,0.28);
        border: none;
    }
    .movie-card {
        background: rgba(255,255,255,0.92);
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.2);
        overflow: hidden;
        box-shadow: 0 10px 24px rgba(15,23,42,0.08);
        padding: 0.6rem;
        height: 100%;
    }
    .movie-card img {
        border-radius: 12px;
    }
    .movie-title {
        margin-top: 0.65rem;
        margin-bottom: 0.2rem;
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.35;
        min-height: 2.7rem;
    }
    .results-heading {
        margin: 1.25rem 0 0.8rem 0;
        font-size: 1.15rem;
        font-weight: 800;
        color: #0f172a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

st.markdown(
    """
    <div class="page-shell">
        <div class="hero">
            <div class="kicker">Movie Recommender</div>
            <h1>CineMatch</h1>
            <p>Pick a title, then get a polished set of similar suggestions with posters and quick visual browsing.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.6, 1], gap="large")

with left:
    st.markdown(
        """
        <div class="panel">
        <h3>Choose your movie</h3>
        <p>Select a title from the dropdown below, then generate similar recommendations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="panel-spacer"></div>', unsafe_allow_html=True)
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Choose a movie",
        movie_list,
        label_visibility="collapsed"
    )
    st.markdown('<div class="panel-spacer"></div>', unsafe_allow_html=True)
    recommend_clicked = st.button('Show Recommendation', use_container_width=True)

with right:
    st.markdown(
        """
        <div class="panel">
        <h3>How it works</h3>
        <p>Select one title and press the button to see five related picks. The layout is now centered and the results are shown as consistent poster cards.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if recommend_clicked:
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    st.markdown('<div class="results-heading">Top matches</div>', unsafe_allow_html=True)
    poster_cols = st.columns(5, gap="medium")
    for col, name, poster in zip(poster_cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster}" style="width: 100%; display: block;" />
                    <div class="movie-title">{name}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )





