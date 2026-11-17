<script lang="ts">
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
    style:--window-width={`${width}%`}
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
                    <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        aria-hidden="true"
                    >
                        <path
                            d={isCollapsed
                                ? 'M9 6l6 6-6 6'
                                : 'M15 6l-6 6 6 6'}
                        />
                    </svg>
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
        flex: var(--window-width) 1 0;
        min-width: 0;
        margin: 0.3rem;
        display: flex;
        justify-content: flex-start;
    }

    .pane {
        box-sizing: border-box;
        width: 100%;
        min-width: 0;
        min-height: 0;
        padding: 1rem;
        border-radius: 10px;
        background: var(--color-backdrop);
        box-shadow:
            0 4px 8px rgba(0, 0, 0, 0.2),
            0 6px 20px rgba(0, 0, 0, 0.19);
        display: flex;
        flex-direction: column;
        transition: width 200ms ease, padding 200ms ease;
    }

    .collapsed .pane {
        width: 48px;
        padding: 6px;
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
        border-radius: 6px;
        background: transparent;
        color: var(--color-text-on-white);
        cursor: pointer;
    }

    button:hover {
        background: rgb(127 127 127 / 15%);
    }

    button:focus-visible {
        outline: 2px solid currentColor;
        outline-offset: 2px;
    }

    hr {
        width: 100%;
        box-sizing: border-box;
        border-color: white;
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

    @media (prefers-reduced-motion: reduce) {
        .pane {
            transition: none;
        }
    }
</style>
