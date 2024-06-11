import { FolderView } from "~/components/FolderView";
import { Match, Switch } from "solid-js";
import { createQuery } from "@tanstack/solid-query";
import { getFolders } from "~/api";
import { BiRegularErrorCircle } from "solid-icons/bi";
import { LegacyConnector } from "~/components/LegacyConnector";




export default function Home() {
  const state = createQuery(() => ({
    queryKey: ["folders"],
    queryFn: getFolders
  }));

  return (
    <main class={"text-gray-500"}>
      <Switch>
        <Match when={state.isError}>
          <div class={"m-12 text-error-900 bg-error-50 border-error-900 p-12 rounded flex flex-row gap-4"}>
            <BiRegularErrorCircle class={"size-6"} />
            <span>
            An unexpected error occurred. (Check the <code class={"font-bold"}>/api.ts</code> file to view the required endpoints.)
            </span>
          </div>
        </Match>
        <Match when={state.isLoading}>
          <div class={"m-12 bg-gray-200 rounded-md h-[300px]"} />
        </Match>
        <Match when={state.isSuccess && state.data}>{
          d => <FolderView root={d()} />
        }</Match>
      </Switch>

      <LegacyConnector/>
    </main>
  );
}
