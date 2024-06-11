import Dialog from "@corvu/dialog";
import { Show } from "solid-js";
import { ImSpinner2 } from "solid-icons/im";

export function RenameModal(props: {
  open: boolean;
  setOpen: (o: boolean) => void;
  onRename: (name: string) => void;
  objectName: string;
  isPending: boolean;
}) {

  return (
    <Dialog open={props.open} onOpenChange={props.setOpen}>
      <Dialog.Portal>
        <Dialog.Overlay class={"fixed bg-opacity-10 inset-0 bg-black grid place-items-center"}>
          <Dialog.Content class={"bg-white p-4 flex flex-col gap-4"}>

            <h2 class={"text-lg font-bold"}>Rename</h2>

            <form class={"flex gap-4  flex-col"}
                  onSubmit={e => {
                    e.preventDefault();
                    const name = (e.currentTarget.elements[0] as HTMLInputElement).value;
                    props.onRename(name);
                  }}>

              <input id={"name"} name={"name"} type={"text"} value={props.objectName}
                     class={"border border-gray-200 p-2"} />


              <div class={"flex gap-4 ml-auto"}>
                <button class={"px-4 py-2 bg-white-500 text-gray-500 hover:bg-gray-200"} type={"button"}
                        onClick={() => props.setOpen(false)}>
                  Cancel
                </button>
                <button
                  class={"px-4 py-2 bg-primary-500 text-white hover:bg-primary-700 flex items-center gap-2"}
                  disabled={props.isPending} type={"submit"}>
                  <Show when={props.isPending}>
                    <ImSpinner2 class={"animate-spin size-4"} />
                  </Show>
                  Rename
                </button>
              </div>

            </form>

          </Dialog.Content>
        </Dialog.Overlay>
      </Dialog.Portal>
    </Dialog>
  );
}