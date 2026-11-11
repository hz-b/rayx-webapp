<script lang="ts">
    import type { Snippet } from 'svelte';

    let { title, width, children }: {
        title: string;
        width: number;
        children: Snippet;
    } = $props();
</script>

<div class="pane" style="width: {width}%;">
    <h2>{title}</h2>
    <hr/>
    <div class="content-container">
        {@render children()}
    </div>
</div>

<style>
    .pane {
        border-radius: 10px;
        padding: 1rem;
        background: var(--color-backdrop);
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin: .3rem;
    }

    .content-container {
        overflow-y: scroll;
    }

    h2 {
        color: var(--color-text-on-white);
        font-size: 1.5rem;
    }

    hr {
        background: gray;
    }

    :global(p) {
        color: var(--color-text-on-white);
    }
</style>
