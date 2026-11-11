<script lang="ts">
    import ContentWindow from "#lib/components/ContentWindow.svelte";
    import Header from "#lib/components/Header.svelte";
    import { IntervalSlider } from "svelte-tweakpane-ui";

    let value: [number, number] = [25, 75]
</script>

<Header/>
<main>
    <ContentWindow title="Settings" width={30}>
        <IntervalSlider
          bind:value
          min={0}
          max={100}
            format={(v) => `${v.toFixed(0)}%`}
        />
    </ContentWindow>
    <ContentWindow title="Graph Viewer" width={70}>
        <p>test</p>
    </ContentWindow>
</main>

<style>
    main{
        margin: 2rem;
        display: flex;
        height: 80vh;
    }
</style>
