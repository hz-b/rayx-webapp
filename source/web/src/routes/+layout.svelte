<script lang="ts">
	import favicon from '#lib/assets/favicon.svg';
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<style>
	:root {
		--color-third-option: #172940;
		--color-primary: #08477B;			/* HZB-Blue */
		--color-secondary: #0F82E1;
		--color-backdrop: #F2F2F2;
		--color-text-on-black: #fff;
		--color-text-on-white: #000;
		--color-label-backdrop: #333;
		--defect: #defec8;

		/* Text */
		--average-text-size: 1rem;
	}

    :global(body) {
		margin: 0;
        font-family: "Roboto", sans-serif;
        font-size: 16px;
        font-weight: 400;
        line-height: 1.5;
        color: inherit;
        background: none;
        -webkit-font-smoothing: antialiased;
    }

    :global(h1),
    :global(h2),
    :global(h3),
    :global(h4),
    :global(h5),
    :global(h6) {
        font-size: inherit;
		color: var(--color-text-on-black)
    }

	:global(h1){
		font-size: 2.5rem;
		font-weight: bold;
		margin: 0;
	}

    :global(h2) {
		font-size: 2rem;
	}
    :global(h3) {
		font-size: 1.75rem;
	}
    :global(h4) {
		font-size: 1.5rem;
	}
    :global(h5) {
		font-size: 1.25rem;
	}
    :global(h6) {
		font-size: 1rem;
	}

    :global(p),
    :global(span),
    :global(label) {
        font: inherit;
		color: var(--color-text-on-black);
		font-size: var(--average-text-size);
    }

    /* Links: no decoration, inherit color */
    :global(a) {
        color: inherit;
        text-decoration: none;
		color: var(--color-text-on-black);
		font-size: var(--average-text-size);
    }

    :global(a:hover),
    :global(a:focus) {
        text-decoration: none;
    }

</style>

{@render children()}
