import { BiRegularDotsVerticalRounded, BiSolidRename } from "solid-icons/bi";
import Popover from "@corvu/popover";
import { AiFillDelete } from "solid-icons/ai";


const buttonStyle = "w-60 p-4 flex gap-4 hover:bg-gray-200 transition duration-200 text-gray-500 items-center";
const iconStyle = "";

export function ContextMenu(props: {
  onDelete: () => void;
  onRename: () => void;
}) {

  return (
    <Popover placement={"left-start"} modal>
      <Popover.Trigger class={"p-4 ml-auto hover:bg-gray-200 focus-within:bg-gray-200 transition duration-200"}>
        <BiRegularDotsVerticalRounded class={"size-6"} />
      </Popover.Trigger>
      <Popover.Portal>
        <Popover.Overlay class={"fixed inset-0 bg-opacity-10 bg-black"} />
        <Popover.Content class="bg-white border border-gray-200 rounded-sm shadow">
          <Popover.Close class={buttonStyle} onClick={props.onDelete}>
            <AiFillDelete class={iconStyle} />
            Delete
          </Popover.Close>

          <Popover.Close class={buttonStyle} onClick={props.onRename}>
            <BiSolidRename class={iconStyle} />
            Rename
          </Popover.Close>
        </Popover.Content>
      </Popover.Portal>
    </Popover>
  );

}