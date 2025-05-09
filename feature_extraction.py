import os
import json
from typing import Optional, List, Dict
import google.generativeai as genai
from dotenv import load_dotenv
import ast

load_dotenv()

genres = ast.literal_eval(os.getenv("GENRES"))
allowed_genres = ", ".join(genres)

PROMPT = f"""
You are an expert movie classification system. You are given a user prompt and your task is to extract:

1. Genres (from a hardcoded list)
2. Language (only if explicitly mentioned)
3. Key Themes of the movie prompt(eg: friendship, revenge, space travel, romance)

### Allowed Genres:
{allowed_genres}

### Example 1:
Prompt: A lighthearted and funny movie  
Output: {{
  "genres": ["Comedy"],
  "specified_language": null,
  "key_themes": "humour, lightheartedness"
}}

### Example 2:
Prompt: A gripping bollywood movie about space and survival  
Output: {{
  "genres": ["Science Fiction", "Drama"],
  "specified_language": "Hindi",
  "key_themes": "space, survival, suspense"
}}

### Now analyze the following prompt:
"""

class FeatureExtractor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI")
        self.model_name = "models/gemini-1.5-flash-latest"  
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    def prompt(self, user_query):
        prompt = PROMPT+f"""
Prompt: {user_query}
Output:
"""
        return prompt
    def extract_features(self, user_prompt: str) -> Dict[str, Optional[List[str]]]:
        prompt = self.prompt(user_prompt)
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            # Parse only the JSON part
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            json_string = text[json_start:json_end]

            result = json.loads(json_string)
            return result
        except Exception as e:
            return {
                "genres": [],
                "specified_language": None,
                "error": str(e)
            }

# TEST        
# f = FeatureExtractor()
# print(f.extract_features("A funny and heartfelt kdrama"))