import psycopg2
from config import parsed_db_url, logger

def get_db_connection():
    """
    Create and return a database connection.
    
    Returns:
        An active database connection
    """
    try:
        return psycopg2.connect(
            dbname=parsed_db_url.path[1:], 
            user=parsed_db_url.username,
            password=parsed_db_url.password,
            host=parsed_db_url.hostname,
            port=parsed_db_url.port
        )
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise