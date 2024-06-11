export async function createFolder(parentId: string): Promise<void> {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v2/folders`, {
    method: "POST",
    body: JSON.stringify({ parentId }),
    headers: {
      "Content-Type": "application/json"
    }
  });

  if (!res.ok) {
    throw new Error("Failed to create folder");
  }
}

export async function getFolders(): Promise<IFolder> {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v2/folders`);

  if (!res.ok) {
    throw new Error("Failed to fetch folders");
  }
  return res.json();
}

export async function editFolder(id: string, name: string): Promise<void> {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v2/folders/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ name }),
    headers: {
      "Content-Type": "application/json"
    }
  });

  if (!res.ok) {
    throw new Error("Failed to edit folder");
  }
}

export async function deleteFolder(id: string): Promise<void> {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v2/folders/${id}`, {
    method: "DELETE"
  });

  if (!res.ok) {
    throw new Error("Failed to delete folder");
  }
}

export async function editDocument(id: string, name: string): Promise<void> {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v2/documents/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ name }),
    headers: {
      "Content-Type": "application/json"
    }
  });

  if (!res.ok) {
    throw new Error("Failed to edit document");
  }
}

export async function createDocument(parentId: string, data: File): Promise<void> {
  const formData = new FormData();
  formData.append("data", data);
  formData.append("parentId", parentId);

  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v2/documents`, {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    throw new Error("Failed to create document");
  }
}

export async function deleteDocument(id: string): Promise<void> {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v2/documents/${id}`, {
    method: "DELETE"
  });

  if (!res.ok) {
    throw new Error("Failed to delete document");
  }
}

export function getDownloadDocumentURL(id: string): string {
  return `${import.meta.env.VITE_BACKEND_URL}/api/v2/documents/${id}`;
}

// --- only relevant for the bonus task ---
export async function pingLegacyEndpoint(): Promise<string> {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v1/ping`);

  if (!res.ok) {
    throw new Error("Legacy not Reached");
  }

  return res.text();
}
