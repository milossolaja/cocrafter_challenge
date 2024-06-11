import { AiFillFolder } from "solid-icons/ai";
import { ContextMenu } from "~/components/ContextMenu";
import { DeleteModal } from "~/components/DeleteModal";
import { createSignal } from "solid-js";
import { RenameModal } from "~/components/RenameModal";
import { createMutation, useQueryClient } from "@tanstack/solid-query";
import { deleteFolder, editFolder } from "~/api";

export function FolderPreview(props: {
  folder: IFolder;
  path: string[];
  setPath: (path: string[]) => void;
}) {

  const [deleteModalOpen, setDeleteModalOpen] = createSignal(false);
  const [renameModalOpen, setRenameModalOpen] = createSignal(false);

  const queryClient = useQueryClient();
  const mutateDelete = createMutation(() => ({
    mutationFn: () => deleteFolder(props.folder.id),
    onSuccess: () => {
      setDeleteModalOpen(false);
      return queryClient.invalidateQueries({
        queryKey: ["folders"]
      });
    }
  }));

  const mutateRename = createMutation(() => ({
    mutationFn: (name: string) => editFolder(props.folder.id, name),
    onSuccess: () => {
      setDeleteModalOpen(false);
      return queryClient.invalidateQueries({
        queryKey: ["folders"]
      });
    }
  }));

  return (
    <>
      <DeleteModal open={deleteModalOpen()} setOpen={setDeleteModalOpen}
                   isPending={mutateDelete.isPending}
                   onDelete={mutateDelete.mutate} objectName={props.folder.name} />

      <RenameModal open={renameModalOpen()} setOpen={setRenameModalOpen}
                   onRename={mutateRename.mutate} isPending={mutateRename.isPending}
                   objectName={props.folder.name} />

      <div class={"shadow border border-gray-200 w-96 flex flex-row bg-white"}>
        <button class={"p-4 flex gap-8 flex-grow hover:bg-gray-200 focus-within:bg-gray-200 transition duration-200"}
                onClick={
                  () => props.setPath(props.path)
                }>
          <AiFillFolder class={"fill-gray-500 size-6"} />
          {props.folder.name}
        </button>
        <ContextMenu onDelete={() => setDeleteModalOpen(true)} onRename={() => setRenameModalOpen(true)} />
      </div>
    </>
  );
}
