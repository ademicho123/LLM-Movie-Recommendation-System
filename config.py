import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
