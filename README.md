# LLM Movie Recommendation System

A simple movie recommendation system that uses The Movie Database (TMDb) API and language models to provide personalized movie suggestions based on user queries.

## Overview

This project combines the power of TMDb's movie database with language models to create an intelligent movie recommendation system. It can:

- Search for movies based on user queries
- Show popular movies
- Display top-rated movies

## Requirements

- Python 3.7+
- API keys for:
  - The Movie Database (TMDb) - Get it from [TMDb website](https://www.themoviedb.org/settings/api)
  - OpenAI - Get it from [OpenAI's platform](https://platform.openai.com/)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/ademicho123/LLM-Movie-Recommendation-System.git
   cd LLM-Movie-Recommendation-System
   ```

2. Install the required packages:
   ```
   pip install requests python-dotenv langchain langchain-openai
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   MOVIE_DB_API_KEY=your_tmdb_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## File Structure

- `main.py` - Main application entry point
- `api_utils.py` - Functions for interacting with TMDb API
- `llm_recommender.py` - Language model integration for query processing
- `config.py` - Configuration and environment variables
- `movie_api_spec.yaml` - OpenAPI specification for TMDb API

## Usage

Run the application with:
```
python main.py
```

You will be prompted to enter a query. Examples:
- "Show me popular movies"
- "What are the top rated movies?"
- "Find movies like Inception"

## API Specification

The `moviedb_doc.yaml` file contains the OpenAPI 3.0 specification for the TMDb API endpoints used in this project. This serves as documentation and can be used with API tools for testing or client generation.

## Error Handling

The application handles cases where movie data might be incomplete, such as missing release dates. It provides fallback values to ensure a smooth user experience.

## Future Improvements

- Add more detailed movie information
- Implement genre filtering
- Add user preferences and personalized recommendations
- Create a web interface
- Expand API coverage to include TV shows

## License

MIT

## Acknowledgments

- [The Movie Database (TMDb)](https://www.themoviedb.org/) for providing the movie data API
- [LangChain](https://langchain.com/) for simplifying LLM integration