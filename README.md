## 🎬 CineMatch

AI-powered movie recommendation engine with semantic search and natural language understanding.

---

## 📌 Overview

CineMatch is an intelligent movie recommendation app that helps you find films based on natural language queries like:

“Show me feel-good comedies like The Intern”

“Sci-fi movies with time travel and a strong female lead”

“Action thrillers released after 2020 with great ratings”

---

### It uses:

- Qdrant Vector Database → stores movie metadata as embeddings for fast semantic search.

- Gemini API → for query interpretation & intent extraction (instead of just “prompt understanding”).

- TMDB API → fetches rich metadata like genres, cast, crew, ratings, and posters.

---

## 🚀 Features

- Natural language query handling

- Vector-based similarity search

- Hybrid filtering (semantic + structured metadata)

- Rich movie info display (from TMDB)

- Easily extensible to support personalization

---

## 🛠️ Tech Stack

- Backend: Python (Streamlit)

- Database: Qdrant

- LLM: Gemini (for intent + keyphrase extraction)

- External API: TMDB (movie data source)

---

## ⚡ Installation

Clone the repo:

```bash
git clone https://github.com/rohraharjas/prompt_to_rec.git
cd prompt_to_rec
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

Add your API keys in .env:

```bash
QDRANT_API_KEY=your_qdrant_api_key
GEMINI_API_KEY=your_gemini_api_key
TMDB_API_KEY=your_tmdb_api_key
```

Run the `data_collection.ipynb` file with your TMDB API to generate `df.csv`

Follow the `VectorSearch.ipynb` file to generate embeddings and migrate your data to QDrant.

Open the application on Streamlit:

`streamlit run app.py`

---

## Demo
[![Demo](https://raw.githubusercontent.com/rohraharjas/prompt_to_rec/main/public/thumbnail.png)](https://raw.githubusercontent.com/rohraharjas/prompt_to_rec/main/public/demo.webm)
