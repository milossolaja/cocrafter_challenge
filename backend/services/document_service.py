import io
import boto3
from fastapi import UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from database import get_db_connection
from config import S3_CONFIG, BUCKET_NAME, logger

# Initialize S3 client
s3 = boto3.client('s3', **S3_CONFIG)

def upload_document(data: UploadFile = Form(...), parent_id: str = Form(...)) -> dict:
    """
    Upload a document to S3 and save its metadata in the database.
    
    Args:
        data (UploadFile): File to upload
        parent_id (str): ID of the parent folder
    
    Returns:
        dict: Uploaded document details
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM documents")
    total_docs = cursor.fetchone()[0]

    doc_id = f"Document-{total_docs + 1}"
    s3_path = f"documents/{doc_id}/{data.filename}"

    try:
        data.file.seek(0)
        s3.upload_fileobj(data.file, BUCKET_NAME, s3_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {str(e)}")
    
    try:
        cursor.execute("""
            INSERT INTO documents (id, name, folder_id, path)
            VALUES (%s, %s, %s, %s)
        """, (doc_id, data.filename, parent_id, s3_path))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save metadata: {str(e)}")
    
    cursor.close()
    conn.close()

    return {"id": doc_id, "name": data.filename, "folderId": parent_id, "path": s3_path}

def get_document(id: str) -> StreamingResponse:
    """
    Retrieve a document from S3.
    
    Args:
        id (str): Document ID
    
    Returns:
        StreamingResponse: File stream for downloading
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, path FROM documents WHERE id = %s", (id,))
    document = cursor.fetchone()

    if not document:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found")
    
    document_name, document_path = document
    cursor.close()
    conn.close()

    try:
        file_stream = io.BytesIO()
        s3.download_fileobj(BUCKET_NAME, document_path, file_stream)
        file_stream.seek(0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve file: {str(e)}")
    
    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{document_name}"'}
    )

def update_document(id: str, name: str) -> dict:
    """
    Update a document's name and path in S3 and database.
    
    Args:
        id (str): Document ID
        name (str): New document name
    
    Returns:
        dict: Updated document details
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT path FROM documents WHERE id = %s", (id,))
    document = cursor.fetchone()

    if not document:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found")

    old_path = document[0]
    new_path = "/".join(old_path.split("/")[:-1]) + f"/{name}"

    try:
        s3.copy_object(Bucket=BUCKET_NAME, 
                       CopySource={"Bucket": BUCKET_NAME, "Key": old_path}, 
                       Key=new_path)
        s3.delete_object(Bucket=BUCKET_NAME, Key=old_path)

        cursor.execute("UPDATE documents SET name = %s, path = %s WHERE id = %s", 
                       (name, new_path, id))
        conn.commit()
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to update document: {str(e)}")
    
    cursor.close()
    conn.close()

    return {"id": id, "name": name, "path": new_path}

def delete_document(id: str) -> dict:
    """
    Delete a document from S3 and database.
    
    Args:
        id (str): Document ID
    
    Returns:
        dict: Deletion confirmation message
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT path FROM documents WHERE id = %s", (id,))
    document = cursor.fetchone()

    if not document:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found")

    document_path = document[0]

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=document_path)

        cursor.execute("DELETE FROM documents WHERE id = %s", (id,))
        conn.commit()
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
    
    cursor.close()
    conn.close()

    return {"message": f"Document {id} was deleted"}