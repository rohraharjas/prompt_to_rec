import streamlit as st
from utils.feature_extraction import FeatureExtractor
from utils.qdrant import QdrantSearch
from utils.poster import get_movie_poster

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Initialize
extractor = FeatureExtractor()
searcher = QdrantSearch()
WATCH_PROVIDERS = [
    "None", "Netflix", "Amazon Prime", "Disney+", "Hulu", "HBO Max", 
    "Apple TV+", "YouTube", "Zee5", "Hotstar", "Sony Liv", "JioCinema"
]

# Sidebar for filters
st.sidebar.header("Preferences")
user_prompt = st.text_area("Describe what you want to watch:", height=120)
watch_provider_selection = st.sidebar.selectbox("Preferred watch provider:", WATCH_PROVIDERS)
watch_provider = None if watch_provider_selection == "None" else watch_provider_selection

if st.button("Find Movies"):
    if not user_prompt.strip():
        st.warning("Please enter a description.")
    else:
        with st.spinner("Extracting features and searching..."):
            extracted = extractor.extract_features(user_prompt)
            results = searcher.search(watch_provider, extracted)

        if results:
            st.success(f"Found {len(results)} movie(s):")
            for result in results:
                title = result.get("title", "Unknown Title")
                overview = result.get("overview", "No description available.")
                language = result.get("language", "N/A")
                providers = result.get("watch_providers", "N/A")
                movie_id = result.get("id")

                col1, col2 = st.columns([1, 3])
                with col1:
                    print(movie_id)
                    poster_url = get_movie_poster(movie_id)
                    if poster_url:
                        if st.button(f"🎬 {title}", key=title):
                            st.session_state[f"{title}_clicked"] = not st.session_state.get(f"{title}_clicked", False)
                        st.image(poster_url, width=150, caption=title)
                with col2:
                    if st.session_state.get(f"{title}_clicked", False):
                        st.markdown(f"**Language:** {language}")
                        st.markdown(f"**Watch Providers:** {providers}")
                        st.markdown("**Overview:**")
                        st.write(overview)
                        st.markdown("---")
        else:
            st.error("No recommendations found. Try a different description.")

# Optional "Go Back" button
if st.button("🔙 Go Back"):
    st.experimental_rerun()
