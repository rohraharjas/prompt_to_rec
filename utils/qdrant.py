from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, SearchRequest
from fastembed.embedding import TextEmbedding
from dotenv import load_dotenv
import os

load_dotenv()

class QdrantSearch:
    def __init__(self):
        url = os.getenv('QDRANT_URL')
        api_key = os.getenv('QDRANT_KEY')
        self.client = QdrantClient(
            url=url,
            api_key=api_key
        )
        self.embedder = TextEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_dir=".cache"
        )

    def embed(self, prompt):
        return list(self.embedder.embed([prompt]))[0]

    def generate_filter(self, genres, lang, wp):
        conditions = []

        # Genre filters
        if genres:
            conditions.extend([
                FieldCondition(
                    key="genres",
                    match=MatchValue(value=genre)
                )
                for genre in genres
            ])

        # Language filter
        if lang:
            conditions.append(
                FieldCondition(
                    key="original_language",
                    match=MatchValue(value=lang)
                )
            )

        # Watch provider filter
        if wp:
            conditions.append(
                FieldCondition(
                    key="watch_providers",
                    match=MatchValue(value=wp)
                )
            )

        return Filter(must=conditions) if conditions else None

    def search(self, watch_provider, extracted_result):
        genres = extracted_result.get('genres', [])
        lang = extracted_result.get('specified_language')
        prompt = ', '.join(extracted_result.get('key_themes', []))

        query_vector = self.embed(prompt)
        query_filter = self.generate_filter(genres, lang, watch_provider)

        results = self.client.search(
            collection_name="movies",
            query_vector=("default", query_vector),
            query_filter=query_filter,
            limit=5
        )

        parsed_results = []
        for r in results:
            parsed_results.append({
                "id": r.payload.get("movie_id"),
                "title": r.payload.get("title", "Unknown Title"),
                "overview": r.payload.get("overview", ""),
                "original_language": r.payload.get("original_language", ""),
                "watch_providers": r.payload.get("watch_providers", []),
                "score": r.score  # Optional: include similarity score
            })

        return parsed_results
