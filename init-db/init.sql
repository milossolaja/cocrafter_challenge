DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS folders;

CREATE TABLE folders (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            parent_id VARCHAR(255) REFERENCES folders(id) ON DELETE CASCADE
        );

CREATE TABLE documents (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            folder_id VARCHAR(255) REFERENCES folders(id) ON DELETE CASCADE,
            path VARCHAR(255) NOT NULL
        );

