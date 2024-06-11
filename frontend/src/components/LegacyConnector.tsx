import { createQuery } from "@tanstack/solid-query";
import { pingLegacyEndpoint } from "~/api";
import { cn } from "~/util";
import { Match, Switch } from "solid-js";
import { ImSpinner2 } from "solid-icons/im";
import { TbPlugConnectedX } from "solid-icons/tb";
import { VsSmiley } from "solid-icons/vs";

export function LegacyConnector() {
  const state = createQuery(() => ({
    queryFn: pingLegacyEndpoint,
    queryKey: ["legacy-backend"]
  }));

  return (
    <div
      class={cn(
        "border border-gray-200 flex flex-row p-6 gap-2 absolute bottom-12 inset-x-12",
        !state.isSuccess && "opacity-50",
        state.isSuccess && "bg-success-50 border-success-500 text-success-500",
        state.isError && "bg-error-50 border-error-500 text-error-500"
      )}
    >
      <Switch>
        <Match when={state.isPending}>
          <ImSpinner2 class={"animate-spin size-6"} />
          <span>Trying to reach the legacy backend</span>
        </Match>
        <Match when={state.isError}>
          <TbPlugConnectedX class={"size-6"} />
          <span>Could not reach the legacy backend</span>
        </Match>
        <Match when={state.isSuccess}>
          <VsSmiley class={"size-6"} />
          <span>Successfully pinged the legacy backend. Good job! :)</span>
        </Match>
      </Switch>
    </div>
  );
}
