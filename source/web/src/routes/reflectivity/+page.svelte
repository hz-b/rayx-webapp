<script lang="ts">
    import ContentWindow from "#lib/components/ContentWindow.svelte";
    import Header from "#lib/components/Header.svelte";
    import ReflectivityTraceSettings from "#lib/components/ReflectivityTraceSettings.svelte";
    import ReflectivityGraph from "#lib/components/ReflectivityGraph.svelte";
</script>

<Header/>
<main>
    <ContentWindow title="Settings" width={30} expandable>
        <ReflectivityTraceSettings endpoint="/api/trace" />
    </ContentWindow>
    <ContentWindow title="Graph Viewer" width={70}>
        <ReflectivityGraph />
    </ContentWindow>
</main>

<style>
    main{
        margin: 2rem;
        display: flex;
        height: 80vh;
    }
</style>
