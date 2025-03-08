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
    
    # Use LLM to format the response in a user-friendly way
    formatted_response = llm.predict(
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
    print(formatted_response)

if __name__ == "__main__":
    main()