from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import StreamingResponse
from typing import Dict, Any
from schemas import UpdateDocumentRequest
from services.document_service import (
    upload_document,
    get_document,
    update_document,
    delete_document
)

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def upload_new_document(data: UploadFile = Form(...), parentId: str = Form(...)):
    """
    Upload a new document to a specific folder.
    
    Args:
        data (UploadFile): File to upload
        parentId (str): ID of the parent folder
    
    Returns:
        Dict[str, Any]: Uploaded document details
    """
    return upload_document(data, parentId)

@router.get("/{id}", response_class=StreamingResponse)
def retrieve_document(id: str):
    """
    Retrieve a document by its ID.
    
    Args:
        id (str): Document ID
    
    Returns:
        StreamingResponse: File stream for downloading
    """
    return get_document(id)

@router.patch("/{id}", response_model=Dict[str, Any])
def modify_document(id: str, request: UpdateDocumentRequest):
    """
    Update a document's name.
    
    Args:
        id (str): Document ID
        request (UpdateDocumentRequest): New document name
    
    Returns:
        Dict[str, Any]: Updated document details
    """
    return update_document(id, request.name)

@router.delete("/{id}", response_model=Dict[str, Any])
def remove_document(id: str):
    """
    Delete a document.
    
    Args:
        id (str): Document ID
    
    Returns:
        Dict[str, Any]: Deletion confirmation message
    """
    return delete_document(id)