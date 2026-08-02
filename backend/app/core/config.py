import os

def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "postgres:password@postgres:543/civicguide")

def get_groq_api_key() -> str:
    """Return the Groq API key from the environment."""
    return os.getenv("GROQ_API_KEY", "")