import os

def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "postgres:password@postgres:543/civicguide")