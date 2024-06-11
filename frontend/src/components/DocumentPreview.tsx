import { AiFillFile } from 'solid-icons/ai';
import { deleteDocument, editDocument, getDownloadDocumentURL } from '~/api';
import { ContextMenu } from '~/components/ContextMenu';
import { createSignal } from 'solid-js';
import { createMutation, useQueryClient } from '@tanstack/solid-query';
import { DeleteModal } from '~/components/DeleteModal';
import { RenameModal } from '~/components/RenameModal';


export function DocumentPreview(props: {
  doc: IDocument
}) {

  const [deleteModalOpen, setDeleteModalOpen] = createSignal(false);
  const [renameModalOpen, setRenameModalOpen] = createSignal(false);

  const queryClient = useQueryClient();
  const mutateDelete = createMutation(() => ({
    mutationFn: () => deleteDocument(props.doc.id),
    onSuccess: () => {
      setDeleteModalOpen(false);
      return queryClient.invalidateQueries({
        queryKey: ['folders'],
      });
    },
  }));

  const mutateRename = createMutation(() => ({
    mutationFn: (name: string) => editDocument(props.doc.id, name),
    onSuccess: () => {
      setDeleteModalOpen(false);
      return queryClient.invalidateQueries({
        queryKey: ['folders'],
      });
    },
  }));


  return (
    <>
      <DeleteModal open={deleteModalOpen()} setOpen={setDeleteModalOpen}
                   isPending={mutateDelete.isPending}
                   onDelete={mutateDelete.mutate} objectName={props.doc.name} />

      <RenameModal open={renameModalOpen()} setOpen={setRenameModalOpen}
                   onRename={mutateRename.mutate} isPending={mutateRename.isPending}
                   objectName={props.doc.name} />

      <div class={'shadow border border-gray-200 w-96 flex flex-row bg-white'}>
        <a class={'p-4 flex gap-8 flex-grow  hover:bg-gray-200'}
           href={getDownloadDocumentURL(props.doc.id)}
           target={'_blank'}>
          <AiFillFile class={'fill-gray-500 size-6'} />
          <span class={'line-clamp-1 overflow-ellipsis'}>
          {props.doc.name}
          </span>
        </a>
        <ContextMenu onDelete={() => setDeleteModalOpen(true)} onRename={() => setRenameModalOpen(true)} />
      </div>
    </>
  );
}
