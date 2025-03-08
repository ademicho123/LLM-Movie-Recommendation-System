from llm_recommender import route_user_query

def main():
    print("Welcome to the AI Movie Recommender!")
    user_query = input("What kind of movie are you looking for? ")
    
    recommendations = route_user_query(user_query)
    
    print("\nHere are some recommendations:")
    for movie in recommendations.get("results", []):
        release_year = "N/A"
        if 'release_date' in movie and movie['release_date']:
            try:
                release_year = movie['release_date'][:4]
            except (IndexError, TypeError):
                release_year = "N/A"
                
        print(f"- {movie['title']} ({release_year})")

if __name__ == "__main__":
    main()