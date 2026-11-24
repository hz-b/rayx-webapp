<script lang="ts">
    import { PanelLeftClose, PanelLeftOpen } from '@lucide/svelte';
    import type { Snippet } from 'svelte';

    let {
        title,
        width,
        expandable = false,
        children
    }: {
        title: string;
        width: number;
        expandable?: boolean;
        children: Snippet;
    } = $props();

    let collapsed = $state(false);

    const isCollapsed = $derived(expandable && collapsed);
</script>

<div
    class="window-slot"
    class:collapsed={isCollapsed}
    style:--window-width={width}
>
    <section class="pane" aria-label={title}>
        <header>
            <h2 hidden={isCollapsed}>{title}</h2>

            {#if expandable}
                <button
                    type="button"
                    onclick={() => (collapsed = !collapsed)}
                    aria-expanded={!isCollapsed}
                    aria-label={`${isCollapsed ? 'Expand' : 'Collapse'} ${title}`}
                    title={`${isCollapsed ? 'Expand' : 'Collapse'} ${title}`}
                >
                    {#if isCollapsed}
                        <PanelLeftOpen />
                    {:else}
                        <PanelLeftClose />
                    {/if}
                </button>
            {/if}
        </header>

        <hr hidden={isCollapsed} />

        <div class="content-container" hidden={isCollapsed}>
            {@render children()}
        </div>
    </section>
</div>

<style>
    .window-slot {
        /* Width is a proportion: for example, 30:70. */
        flex: var(--window-width) 1 0;
        min-width: 0;
        margin: 0.3rem;
        display: flex;
        justify-content: flex-start;
    }

    .window-slot.collapsed {
        flex: 0 0 3rem;
    }

    .pane {
        box-sizing: border-box;
        width: 100%;
        min-width: 0;
        min-height: 0;
        padding: 1rem;
        border-radius: 0.625rem;
        background: var(--color-backdrop);
        box-shadow:
            0 0.25rem 0.5rem rgb(0 0 0 / 20%),
            0 0.375rem 1.25rem rgb(0 0 0 / 19%);
        display: flex;
        flex-direction: column;
    }

    header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        flex-shrink: 0;
    }

    .collapsed header {
        justify-content: center;
    }

    h2 {
        margin: 0;
        min-width: 0;
        overflow-wrap: anywhere;
        color: var(--color-text-on-white);
        font-size: 1.5rem;
    }

    button {
        width: 2.25rem;
        height: 2.25rem;
        flex-shrink: 0;
        display: grid;
        place-items: center;
        padding: 0;
        border: none;
        border-radius: 0.375rem;
        background: transparent;
        color: var(--color-text-on-white);
        cursor: pointer;
    }

    button:hover {
        background: rgb(127 127 127 / 15%);
    }

    button:focus-visible {
        outline: 0.125rem solid currentColor;
        outline-offset: 0.125rem;
    }

    svg {
        width: 1.25rem;
        height: 1.25rem;
    }

    hr {
        width: 100%;
        box-sizing: border-box;
        border: 0;
        border-top: 0.0625rem solid gray;
        margin: 0.75rem 0;
    }

    .content-container {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
    }

    [hidden] {
        display: none;
    }

    .content-container :global(p) {
        color: var(--color-text-on-white);
    }
</style>
