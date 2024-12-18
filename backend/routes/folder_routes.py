from fastapi import APIRouter
from typing import Dict, Any
from schemas import CreateFolderRequest, EditFolderRequest
from services.folder_service import (
    get_folder_hierarchy, 
    create_new_folder, 
    update_folder, 
    delete_folder
)

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
def get_folders():
    """
    Retrieve the entire folder hierarchy.
    
    Returns:
        Dict[str, Any]: Root folder with nested children and documents
    """
    return get_folder_hierarchy()

@router.post("/", response_model=Dict[str, Any])
def create_folder(request: CreateFolderRequest):
    """
    Create a new folder.
    
    Args:
        request (CreateFolderRequest): Parent folder ID for the new folder
    
    Returns:
        Dict[str, Any]: Details of the newly created folder
    """
    return create_new_folder(request.parentId)

@router.patch("/{id}", response_model=Dict[str, Any])
def update_folder_name(id: str, request: EditFolderRequest):
    """
    Update the name of an existing folder.
    
    Args:
        id (str): ID of the folder to update
        request (EditFolderRequest): New folder name
    
    Returns:
        Dict[str, Any]: Updated folder details
    """
    return update_folder(id, request.name)

@router.delete("/{id}", response_model=Dict[str, Any])
def remove_folder(id: str):
    """
    Delete a folder and its contents recursively.
    
    Args:
        id (str): ID of the folder to delete
    
    Returns:
        Dict[str, Any]: Deletion confirmation message
    """
    return delete_folder(id)