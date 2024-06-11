import { AiFillFolderAdd } from 'solid-icons/ai';
import { primaryButton } from '~/components/styles';
import { createMutation, useQueryClient } from '@tanstack/solid-query';
import { createFolder } from '~/api';
import { Match, Switch } from 'solid-js';
import { ImSpinner2 } from 'solid-icons/im';
import { BiRegularErrorCircle } from 'solid-icons/bi';

export function AddFolderButton(props: {
  parentId: string;
}) {
  const queryClient = useQueryClient();
  const mutation = createMutation(() => ({
    mutationFn: async () => createFolder(props.parentId),
    onSuccess: () => {
      return queryClient.invalidateQueries({
        queryKey: ['folders'],
      });
    },
  }));

  return (
    <button class={primaryButton} onClick={() => mutation.mutate()} disabled={mutation.isPending}>
      <Switch>
        <Match when={mutation.isError}>
          <BiRegularErrorCircle class={'size-6'} />
        </Match>
        <Match when={mutation.isPending}>
          <ImSpinner2 class={'animate-spin size-6'} />
        </Match>
        <Match when={true}>
          <AiFillFolderAdd class={'size-6'} />
        </Match>
      </Switch>
      Add Folder
    </button>
  );
}