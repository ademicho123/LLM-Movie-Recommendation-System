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

# Create enhanced API Chain
api_docs = load_api_docs()
api_chain = APIChain.from_llm_and_api_docs(
    llm=llm,
    api_docs=api_docs,
    prompt=movie_api_prompt,
    headers={"Authorization": f"Bearer {MOVIE_DB_API_KEY}"},
    limit_to_domains=["api.themoviedb.org"]
)

def process_movie_request(user_query):
    """
    Process user's movie request through the LLM and API Chain.
    This lets the LLM determine which endpoint to use based on understanding the query.
    """
    try:
        # Run the query through the API Chain
        response = api_chain.run(user_query)
        return response
    except Exception as e:
        print(f"Error processing request: {e}")
        # Fallback to direct API calls if the chain fails
        from api_utils import search_movie, get_popular_movies, get_top_rated_movies
        
        if "popular" in user_query.lower():
            return get_popular_movies()
        elif "top rated" in user_query.lower() or "best" in user_query.lower():
            return get_top_rated_movies()
        else:
            return search_movie(user_query)