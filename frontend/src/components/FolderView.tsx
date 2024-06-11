import { FolderPreview } from "~/components/FolderPreview";
import { createMemo, createSignal, For, Show } from "solid-js";
import { DocumentPreview } from "~/components/DocumentPreview";
import { AddFolderButton } from "~/components/AddFolderButton";
import { AddDocumentButton } from "~/components/AddDocumentButton";


export function FolderView(props: { root: IFolder }) {

  const [path, setPath] = createSignal<string[]>([props.root.id]);

  const folderPath = createMemo(() => {
    const p = path().slice(1);
    return p.reduce<IFolder[]>((acc, id) => {
      const last: IFolder = acc[acc.length - 1];
      const next = last.children.find(f => f.id === id);
      if (next) {
        acc.push(next);
      }
      return acc;
    }, [props.root]);
  });
  const selectedFolder = createMemo(() => folderPath()[folderPath().length - 1]);

  return (
    <>
      <nav class={"p-12 pb-0 flex flex-wrap items-center"}>
        <For each={folderPath()}>{(navItem, index) =>
          <>
            <Show when={index() !== folderPath().length - 1}
                  fallback={<span class={"font-bold"}>{navItem.name}</span>}
            >
              <button
                class={"hover:underline"}
                onClick={
                  () => {
                    setPath(p => p.slice(0, index() + 1));
                  }
                }>
                {navItem.name}
              </button>
              <span class={"mx-1"}>/</span>
            </Show>

          </>
        }</For>
      </nav>

      <section class="flex flex-row flex-wrap gap-4 p-12 pb-0">
        <AddFolderButton parentId={selectedFolder().id} />
        <For each={selectedFolder().children}>{child =>
          <FolderPreview path={
            [...path(), child.id]
          } setPath={setPath} folder={child} />
        }</For>
      </section>

      <section class="flex flex-row flex-wrap gap-4 p-12">
        <AddDocumentButton parentId={selectedFolder().id} />
        <For each={selectedFolder().documents}>{doc =>
          <DocumentPreview doc={doc} />
        }</For>
      </section>
    </>


  );

}