import psycopg2
from urllib.parse import urlparse

DATABASE_URL = "postgres://postgres:postgres@db:5432/db"

result = urlparse(DATABASE_URL)

def create_database_and_tables():
    conn = psycopg2.connect(
        dbname=result.path[1:],  
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS documents")
    cursor.execute("DROP TABLE IF EXISTS folders")

    cursor.execute("""
        CREATE TABLE folders (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            parent_id VARCHAR(255) REFERENCES folders(id) ON DELETE CASCADE
        );
        """)

    cursor.execute("""
        CREATE TABLE documents (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            folder_id VARCHAR(255) REFERENCES folders(id) ON DELETE CASCADE,
            path VARCHAR(255) NOT NULL
        );
        """)


    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database_and_tables()