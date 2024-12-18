from pydantic import BaseModel

class CreateFolderRequest(BaseModel):
    parentId: str

class EditFolderRequest(BaseModel):
    name: str

class UpdateDocumentRequest(BaseModel):
    name: str