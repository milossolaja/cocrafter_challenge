import Dialog from "@corvu/dialog";
import { Show } from "solid-js";
import { ImSpinner2 } from "solid-icons/im";

export function DeleteModal(props: {
  open: boolean;
  setOpen: (o: boolean) => void;
  onDelete: () => void;
  objectName: string;
  isPending: boolean;
}) {

  return (
    <Dialog open={props.open} onOpenChange={props.setOpen}>
      <Dialog.Portal>
        <Dialog.Overlay class={"fixed bg-opacity-10 inset-0 bg-black grid place-items-center"}>
          <Dialog.Content class={"bg-white p-4 flex flex-col gap-4"}>

            <h2 class={"text-lg font-bold"}>Are you sure you want to delete "{props.objectName}"?</h2>

            <div class={"flex gap-4 ml-auto"}>
              <button class={"px-4 py-2 bg-white-500 text-gray-500 hover:bg-gray-200"}
                      type={"button"}
                      onClick={() => props.setOpen(false)}>
                Cancel
              </button>
              <button class={"px-4 py-2 bg-primary-500 text-white hover:bg-primary-700 flex gap-2"}
                      type={"button"}
                      disabled={props.isPending}
                      onClick={() => {
                        props.onDelete();
                      }}>
                <Show when={props.isPending}>
                  <ImSpinner2 class={"animate-spin size-6"} />
                </Show>
                Delete
              </button>

            </div>

          </Dialog.Content>
        </Dialog.Overlay>
      </Dialog.Portal>
    </Dialog>
  );
}