from typing import Dict, Any
from database import get_db_connection
from config import logger

def get_folder_hierarchy() -> Dict[str, Any]:
    """
    Retrieve the entire folder hierarchy from the database.
    
    Returns:
        Dict[str, Any]: Root folder with nested children and documents
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ensure root folder exists
    cursor.execute("SELECT * FROM folders WHERE parent_id IS NULL")
    root_folder = cursor.fetchone()

    if not root_folder:
        cursor.execute("INSERT INTO folders (id, name, parent_id) VALUES ('root', 'root' , NULL)")
        conn.commit()

    # Fetch all folders and documents
    cursor.execute("SELECT * FROM folders")
    folders = cursor.fetchall()
    folder_columns = [desc[0] for desc in cursor.description]

    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()
    document_columns = [desc[0] for desc in cursor.description]

    # Convert to dictionaries
    folders = [dict(zip(folder_columns, folder)) for folder in folders]
    documents = [dict(zip(document_columns, document)) for document in documents]

    # Create folder map
    folder_map = {folder["id"]: {**folder, "children": [], "documents": []} for folder in folders}
    
    # Assign documents to folders
    for document in documents:
        if document["folder_id"]:
            folder_map[document["folder_id"]]["documents"].append(document)

    # Build hierarchy
    for folder in folders:
        if folder["parent_id"]:
            folder_map[folder["parent_id"]]["children"].append(folder_map[folder["id"]])

    cursor.close()
    conn.close()

    return folder_map['root']

def create_new_folder(parent_id: str) -> Dict[str, str]:
    """
    Create a new folder with an auto-generated ID.
    
    Args:
        parent_id (str): ID of the parent folder
    
    Returns:
        Dict[str, str]: Details of the newly created folder
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM folders WHERE parent_id = %s ORDER BY id ASC", (parent_id,))
        child_ids = cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching child folders: {e}")
        raise

    # Generate new folder ID
    if parent_id == "root" and not child_ids:
        new_id = "Folder-1"  
    elif parent_id == "root" and child_ids:
        last_child_id = child_ids[-1][0]
        last_suffix = int(last_child_id.split('-')[-1]) + 1
        new_id = f"Folder-{last_suffix}"  
    elif not child_ids:
        new_id = f"{parent_id}-1"
    else:
        last_child_id = child_ids[-1][0]
        last_suffix = int(last_child_id.split('-')[-1]) + 1
        new_id = f"{parent_id}-{last_suffix}"
    
    try:
        cursor.execute(
            "INSERT INTO folders (id, name, parent_id) VALUES (%s, %s, %s)",
            (new_id, new_id, parent_id),
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Error creating folder: {e}")
        raise

    cursor.close()
    conn.close()

    return {"id": new_id, "name": new_id, "parentId": parent_id}

def update_folder(id: str, name: str) -> Dict[str, str]:
    """
    Update a folder's name.
    
    Args:
        id (str): Folder ID
        name (str): New folder name
    
    Returns:
        Dict[str, str]: Updated folder details
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE folders SET name = %s WHERE id = %s",
        (name, id),
    )
    conn.commit()

    cursor.close()
    conn.close()

    return {"id": id, "name": name}

def delete_folder(id: str) -> Dict[str, str]:
    """
    Delete a folder and its contents recursively.
    
    Args:
        id (str): Folder ID to delete
    
    Returns:
        Dict[str, str]: Deletion confirmation message
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        BEGIN;
        WITH RECURSIVE folder_tree AS (
            SELECT id
            FROM folders
            WHERE id = %s
            UNION ALL
            SELECT f.id
            FROM folders f
            INNER JOIN folder_tree ft ON f.parent_id = ft.id
        ),
        documents_to_delete AS (
            SELECT d.id
            FROM documents d
            WHERE d.folder_id IN (
                SELECT id 
                FROM folder_tree
            )
        )
        DELETE FROM documents
        WHERE id IN (SELECT id FROM documents_to_delete);

        WITH RECURSIVE folder_tree AS (
            SELECT id
            FROM folders
            WHERE id = %s
            UNION ALL
            SELECT f.id
            FROM folders f
            INNER JOIN folder_tree ft ON f.parent_id = ft.id
        )
        DELETE FROM folders
        WHERE id IN (
            SELECT id 
            FROM folder_tree
        );
        COMMIT;
        """, (id, id))

    conn.commit()

    cursor.close()
    conn.close()
    
    return {"message": f"Folder {id} and its contents were deleted"}