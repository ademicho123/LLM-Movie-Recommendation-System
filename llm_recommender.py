from langchain.chains.api.base import APIChain
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from api_utils import search_movie, get_popular_movies, get_top_rated_movies

# Initialize OpenAI Model
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# API Documentation for Movie Database API
api_docs = """
BASE_URL: https://api.themoviedb.org/3
ENDPOINTS:
  - /search/movie?query=<movie_name>&api_key=<API_KEY>
  - /movie/popular?api_key=<API_KEY>
  - /movie/top_rated?api_key=<API_KEY>
"""

# Create API Chain
api_chain = APIChain.from_llm_and_api_docs(llm, api_docs, limit_to_domains=["https://api.themoviedb.org"])

def route_user_query(user_query):
    """Determine the correct API endpoint based on user input."""
    if "popular" in user_query.lower():
        return get_popular_movies()
    elif "top rated" in user_query.lower():
        return get_top_rated_movies()
    else:
        return search_movie(user_query)