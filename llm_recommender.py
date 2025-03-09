import os
import yaml
from langchain.chains.api.base import APIChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import OPENAI_API_KEY, MOVIE_DB_API_KEY

# Initialize OpenAI Model
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# Load OpenAPI spec from YAML file
def load_api_docs():
    yaml_path = os.path.join(os.path.dirname(__file__), 'moviedb_doc.yaml')
    with open(yaml_path, 'r') as file:
        spec = yaml.safe_load(file)
    
    # Convert to string format expected by LangChain
    api_docs = f"""
    BASE_URL: {spec['servers'][0]['url']}
    
    ENDPOINTS:
    """
    
    # Add each endpoint from the spec
    for path, methods in spec['paths'].items():
        for method, details in methods.items():
            api_docs += f"  - {method.upper()} {path}\n"
            api_docs += f"    Description: {details.get('description', details.get('summary', ''))}\n"
            
            # Add parameters
            if 'parameters' in details:
                api_docs += "    Parameters:\n"
                for param in details['parameters']:
                    api_docs += f"      - {param['name']} ({param['in']}): {param.get('description', '')}\n"
    
    return api_docs

# Define custom prompt template for movie queries
movie_api_prompt = PromptTemplate(
    input_variables=["query", "api_docs"],
    template="""
    You are an AI assistant that helps users find movies using the Movie Database API.
    Based on the user's request, determine which API endpoint to use and how to format the request.
    
    User Request: {query}
    
    API Documentation:
    {api_docs}
    
    Your task is to:
    1. Determine which API endpoint best matches the user's request
    2. Format the request properly for that endpoint
    3. Include the API key parameter in your request
    
    API Request:
    """
)

# Extract movie keywords for better searching
def extract_keywords(user_query):
    """Extract relevant keywords from a user query for better movie search"""
    # Map common request patterns to relevant search terms
    query_mapping = {
        "laugh": "comedy",
        "funny": "comedy",
        "scare": "horror",
        "scary": "horror",
        "action": "action",
        "thrill": "thriller",
        "romantic": "romance",
        "love story": "romance",
        "scifi": "science fiction",
        "sci-fi": "science fiction",
        "science fiction": "science fiction",
        "drama": "drama",
        "documentary": "documentary",
        "animation": "animation",
        "cartoon": "animation",
        "family": "family"
    }
    
    # Convert query to lowercase for matching
    query_lower = user_query.lower()
    
    # Check for keyword matches
    for key, value in query_mapping.items():
        if key in query_lower:
            return value
    
    # If no specific matches, return the original query but remove common phrases
    cleaned_query = query_lower.replace("i want", "").replace("movie that will", "").replace("looking for", "")
    cleaned_query = cleaned_query.replace("i'm looking for", "").replace("can you recommend", "")
    cleaned_query = cleaned_query.strip()
    
    return cleaned_query

def process_movie_request(user_query):
    """
    Process user's movie request through the LLM and API Chain.
    This lets the LLM determine which endpoint to use based on understanding the query.
    """
    try:
        # If the query is about popular or top-rated movies, use those endpoints
        if "popular" in user_query.lower():
            from api_utils import get_popular_movies
            return get_popular_movies()
        elif "top rated" in user_query.lower() or "best" in user_query.lower():
            from api_utils import get_top_rated_movies
            return get_top_rated_movies()
        
        # For generic queries, extract keywords and use search
        from api_utils import search_movie
        search_term = extract_keywords(user_query)
        print(f"Searching for: {search_term}")
        return search_movie(search_term)
        
    except Exception as e:
        print(f"Error processing request: {e}")
        # Fallback to direct API calls with extracted keywords
        from api_utils import search_movie
        
        search_term = extract_keywords(user_query)
        print(f"Fallback search for: {search_term}")
        return search_movie(search_term)