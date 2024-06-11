interface IDocument {
  id: string,
  name: string,
}

interface IFolder {
  id: string,
  name: string,
  children: IFolder[],
  documents: IDocument[],
}