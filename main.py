from llm_recommender import process_movie_request
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

# Initialize OpenAI Model for response formatting
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

def main():
    print("Welcome to the AI Movie Recommender!")
    user_query = input("What kind of movie are you looking for? ")
    
    # Get raw API response
    api_response = process_movie_request(user_query)
    
    # Check if the API response is valid
    if not api_response or "results" not in api_response:
        print("\nSorry, we couldn't find any movies matching your request.")
        return
    
    # Use LLM to format the response in a user-friendly way
    formatted_response = llm.invoke(
        f"""
        Based on the user's request: "{user_query}"
        
        Here is the raw API response: {api_response}
        
        Please format this into a user-friendly list of movie recommendations.
        For each movie, include:
        - Title and year
        - A brief description (if available)
        - Rating (if available)
        
        Limit to the top 5 most relevant movies.
        """
    )
    
    print("\nHere are your personalized movie recommendations:")
    # Extract just the content from the response
    if hasattr(formatted_response, 'content'):
        print(formatted_response.content)
    else:
        print(str(formatted_response))

if __name__ == "__main__":
    main()