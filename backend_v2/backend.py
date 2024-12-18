from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from urllib.parse import urlparse
from typing import Dict, Any
import logging
import boto3
import io


DATABASE_URL = "postgres://postgres:postgres@db:5432/db"

result = urlparse(DATABASE_URL)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.client('s3', 
    endpoint_url='http://s3mock:9090', 
    region_name='us-east-1',
    aws_access_key_id='dummy_access_key',
    aws_secret_access_key='dummy_secret_key'
    )

try:  
    response = s3.head_bucket(Bucket='cocrafter-dev')
    print(f"Bucket cocrafter-dev already exists.")
except:
    s3.create_bucket(Bucket='cocrafter-dev')


# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=result.path[1:], 
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

class CreateFolderRequest(BaseModel):
    parentId: str

class EditFolderRequest(BaseModel):
    name: str

class UpdateDocumentRequest(BaseModel):
    name: str

def getFolderHierarchy() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM folders WHERE parent_id IS NULL")
    root_folder = cursor.fetchone()

    if not root_folder:
        cursor.execute("INSERT INTO folders (id, name, parent_id) VALUES ('root', 'root' , NULL)")
        conn.commit()

    cursor.execute("SELECT * FROM folders")
    folders = cursor.fetchall()

    folder_columns = [desc[0] for desc in cursor.description]

    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()

    document_columns = [desc[0] for desc in cursor.description]

    folders = [dict(zip(folder_columns, folder)) for folder in folders]
    documents = [dict(zip(document_columns, document)) for document in documents]

    folder_map = {folder["id"]: {**folder, "children": [], "documents": []} for folder in folders}
    
    for document in documents:
        if document["folder_id"]:
            folder_map[document["folder_id"]]["documents"].append(document)

    for folder in folders:
        if folder["parent_id"]:
            folder_map[folder["parent_id"]]["children"].append(folder_map[folder["id"]])

    cursor.close()
    conn.close()

    return folder_map['root']

def createNewFolder(parent_id):
    #logger.info(f"Creating new folder with parent_id: {parent_id}")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM folders WHERE parent_id = %s ORDER BY id ASC",
            (parent_id,),
        )
        child_ids = cursor.fetchall()
    except Exception as e:
        logger.error(f"Error: {e}")

    if parent_id == "root" and not child_ids:
        new_id = "Folder-1"  
    elif parent_id == "root" and child_ids:
        last_child_id = child_ids[-1][0]
        last_parts = last_child_id.split('-')
        last_suffix = int(last_parts[-1]) + 1
        new_id = f"Folder-{last_suffix}"  
    elif not child_ids:
        new_id = f"{parent_id}-1"
    else:
        last_child_id = child_ids[-1][0]
        last_parts = last_child_id.split('-')
        last_suffix = int(last_parts[-1]) + 1
        new_id = f"{parent_id}-{last_suffix}"
    
    try:
        cursor.execute(
                "INSERT INTO folders (id, name, parent_id) VALUES (%s, %s, %s)",
                (new_id, new_id, parent_id),
            )
        conn.commit()
    except Exception as e:
        logger.error(f"Error: {e}")

    cursor.close()
    conn.close()

    return {"id": new_id, "name": new_id, "parentId": parent_id}

def updateFolder(id:str, request):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
            "UPDATE folders SET name = %s WHERE id = %s",
            (request.name, id),
        )
    conn.commit()

    cursor.close()
    conn.close()

    return {"id": id, "name": request.name}

def deleteFolder(id: str):
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

def uploadDocument(data: UploadFile = Form(...), parentId: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM documents")
    total_docs = cursor.fetchone()[0]

    doc_id = f"Document-{total_docs + 1}"

    s3_path = f"documents/{doc_id}/{data.filename}"

    try:
        data.file.seek(0)
        s3.upload_fileobj(data.file, 'cocrafter-dev', s3_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {str(e)}")
    
    try:
        cursor.execute("""
            INSERT INTO documents (id, name, folder_id, path)
            VALUES (%s, %s, %s, %s)
        """, (doc_id, data.filename, parentId, s3_path))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save metadata: {str(e)}")
    
    cursor.close()
    conn.close()

    return {"id": doc_id, "name": data.filename, "folderId": parentId, "path": s3_path}

def getDocument(id: str):
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
        s3.download_fileobj('cocrafter-dev', document_path, file_stream)
        file_stream.seek(0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve file: {str(e)}")
    
    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{document_name}"'}
    )

def updateDocument(id: str, name: str):
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
        s3.copy_object(Bucket="cocrafter-dev", CopySource={"Bucket": "cocrafter-dev", "Key": old_path}, Key=new_path)
        s3.delete_object(Bucket="cocrafter-dev", Key=old_path)

        cursor.execute("UPDATE documents SET name = %s, path = %s WHERE id = %s", (name, new_path, id))
        conn.commit()
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to update document: {str(e)}")
    
    cursor.close()
    conn.close()

    return {"id": id, "name": name, "path": new_path}

def deleteDocument(id: str):
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
        s3.delete_object(Bucket="cocrafter-dev", Key=document_path)

        cursor.execute("DELETE FROM documents WHERE id = %s", (id,))
        conn.commit()
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
    
    cursor.close()
    conn.close()

    return {"message": f"Document {id} was deleted"}

# Routes
@app.get("/api/v2/folders", response_model=Dict[str, Any])
def get_folders():
    return getFolderHierarchy()

@app.post("/api/v2/folders", response_model=Dict[str, Any])
def create_folder(request : CreateFolderRequest):
    return createNewFolder(request.parentId)

@app.patch("/api/v2/folders/{id}", response_model=Dict[str, Any])
def update_folder(id: str, request: EditFolderRequest):
    return updateFolder(id, request)

@app.delete("/api/v2/folders/{id}", response_model=Dict[str, Any])
def delete_folder(id: str):
    return deleteFolder(id)

@app.post("/api/v2/documents", response_model=Dict[str, Any])
def upload_document(data: UploadFile = Form(...), parentId: str = Form(...)):
    return uploadDocument(data, parentId)

@app.get("/api/v2/documents/{id}", response_class=StreamingResponse)
def get_document(id: str):
    return getDocument(id)

@app.patch("/api/v2/documents/{id}", response_model=Dict[str, Any])
def update_document(id: str, request: UpdateDocumentRequest):
    return updateDocument(id, request.name)

@app.delete("/api/v2/documents/{id}", response_model=Dict[str, Any])
def delete_document(id: str):
    return deleteDocument(id)
