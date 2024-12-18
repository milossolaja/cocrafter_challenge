from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
from typing import Dict, Any
from fastapi import Form, UploadFile
from fastapi.responses import StreamingResponse
from schemas import CreateFolderRequest, EditFolderRequest, UpdateDocumentRequest

from services.folder_service import (
    get_folder_hierarchy, 
    create_new_folder, 
    update_folder, 
    delete_folder
)
from services.document_service import (
    upload_document,
    get_document,
    update_document,
    delete_document
)

from config import S3_CONFIG, BUCKET_NAME
from routes import folder_routes, document_routes

# Initialize FastAPI application
app = FastAPI(
    title="CoCrafter Document Management API",
    description="API for managing folders and documents with S3 storage",
    version="2.0.0",
    redirect_slashes=False
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize S3 client and ensure bucket exists
s3 = boto3.client('s3', **S3_CONFIG)

try:  
    s3.head_bucket(Bucket=BUCKET_NAME)
    print(f"Bucket {BUCKET_NAME} already exists.")
except:
    s3.create_bucket(Bucket=BUCKET_NAME)

# Routes
@app.get("/api/v2/folders", response_model=Dict[str, Any])
def get_folders():
    return get_folder_hierarchy()

@app.post("/api/v2/folders", response_model=Dict[str, Any])
def create_folder(request : CreateFolderRequest):
    return create_new_folder(request.parentId)

@app.patch("/api/v2/folders/{id}", response_model=Dict[str, Any])
def update_folder_name(id: str, request: EditFolderRequest):
    return update_folder(id, request.name)

@app.delete("/api/v2/folders/{id}", response_model=Dict[str, Any])
def remove_folder(id: str):
    return delete_folder(id)

@app.post("/api/v2/documents", response_model=Dict[str, Any])
def upload_new_document(data: UploadFile = Form(...), parentId: str = Form(...)):
    return upload_document(data, parentId)

@app.get("/api/v2/documents/{id}", response_class=StreamingResponse)
def retrieve_document(id: str):
    return get_document(id)

@app.patch("/api/v2/documents/{id}", response_model=Dict[str, Any])
def modify_document(id: str, request: UpdateDocumentRequest):
    return update_document(id, request.name)

@app.delete("/api/v2/documents/{id}", response_model=Dict[str, Any])
def remove_document(id: str):
    return delete_document(id)
