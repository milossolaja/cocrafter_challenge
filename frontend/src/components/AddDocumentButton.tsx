import { AiFillFileAdd } from 'solid-icons/ai';
import { primaryButton } from '~/components/styles';
import { cn } from '~/util';
import { createMutation, useQueryClient } from '@tanstack/solid-query';
import { createDocument } from '~/api';
import { Match, Switch } from 'solid-js';
import { ImSpinner2 } from 'solid-icons/im';
import { BiRegularErrorCircle } from 'solid-icons/bi';

export function AddDocumentButton(props: {
  parentId: string;
}) {

  const queryClient = useQueryClient();
  const mutation = createMutation(() => ({
    mutationFn: async (data: File) => createDocument(props.parentId, data),
    onSuccess: () => {
      return queryClient.invalidateQueries({
        queryKey: ['folders'],
      });
    },
  }));

  return (
    <label
      class={cn(
        primaryButton, 'cursor-pointer focus-within:rounded-sm focus-within:outline outline-black -outline-offset-1',
      )}
    >
      <Switch>
        <Match when={mutation.isError}>
          <BiRegularErrorCircle class={'size-6'} />
        </Match>
        <Match when={mutation.isPending}>
          <ImSpinner2 class={'animate-spin size-6'} />
        </Match>
        <Match when={true}>
          <AiFillFileAdd class={'size-6'} />
        </Match>
      </Switch>
      Add File
      <input disabled={mutation.isPending} type={'file'} class={'sr-only'}
             onChange={e => {
               if (!e.target.files) return;
               mutation.mutate(e.target.files[0]);
               e.target.value = '';
             }}
      />
    </label>
  );
}